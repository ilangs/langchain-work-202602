# main(repeat).py파일

import os, json, asyncio, httpx
from typing import TypedDict
from dotenv import load_dotenv
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.graph import StateGraph

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


# [1] 설정 로드: API 키와 환경 변수 관리
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# [2] FastAPI 서버 객체 생성 및 정적 경로 설정
app = FastAPI()

# 현재 main.py 파일이 위치한 디렉토리의 절대 경로를 구합니다.
BASE_DIR = Path(__file__).resolve().parent
# static 폴더 안의 CSS 파일을 브라우저가 읽을 수 있게 마운트
app.mount("/static", StaticFiles(directory=str(BASE_DIR/"static")), name="static")
# templates 폴더 설정 (HTML 파일 위치)
templates = Jinja2Templates(directory=str(BASE_DIR/"templates"))

# [3] AI 모델 초기화 (속도와 정확도의 밸런스가 좋은 gpt-4o-mini)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# [4] 데이터 통로 정의 (에이전트가 들고 다닐 바구니)
class AgentState(TypedDict):
    user_input: str       # 사용자 질문
    emotion: dict         # 분석된 감정 데이터
    genre: int            # 결정된 영화 장르 코드
    recommendations: list # 최종 추천 리스트

# [5] 감정 분석 도구: 심리학자 페르소나 강화
@tool
async def emotion_tool(text: str) -> dict:
    """사용자의 심리를 분석하여 따뜻한 공감 문장을 생성합니다."""
    prompt = f"""
    당신은 30년 경력의 심리학 박사이자 영화 치료 전문가입니다.
    사용자의 말에 깊이 공감하고, 영화를 추천하는 이유를 '세로로 읽기 편하게' 짧은 호흡의 문장으로 작성하세요.
    
    반드시 아래 JSON 형식으로만 답변하세요:
    {{
        "감정": "행복/슬픔/분노/설렘/기본",
        "공감멘트": "마음이 많이 지치셨군요. / 잠시 쉬어가도 괜찮아요. / 당신을 위한 영화입니다."
    }}
    입력: "{text}"
    """
    res = await llm.ainvoke(prompt)
    try:
        # JSON 문자열만 추출하여 파이썬 딕셔너리로 변환
        content = res.content.replace("```json", "").replace("```", "").strip() #전처리(""로 변경)
        return json.loads(content)
    except: # 위에서 처리하지 못하는 경우 기본 설정값으로 처리
        return {"감정": "기본", "공감멘트": "당신의 기분에 딱 맞는 / 좋은 영화를 준비했습니다."}

# [6] 영화 추천 도구: 고득점 명작 위주
@tool
async def recommend_tool(genre: int, emotion: dict) -> list:
    """TMDB에서 검증된 명작 5편을 가져옵니다."""
    async with httpx.AsyncClient() as client:
        res = await client.get(
            "https://api.themoviedb.org/3/discover/movie",
            params={
                "api_key": TMDB_API_KEY,
                "language": "ko-KR",
                "with_genres": genre,
                "vote_average.gte": 7.0,      # 평점 7점 이상만
                "sort_by": "popularity.desc"  # 인기순 정렬
            }
        )
        data = res.json()
        # 프론트엔드 디자인을 위해 데이터를 정제해서 보냄
        return [{
            "title": m["title"],
            "desc": m.get("overview", "설명 없음")[:60] + "...", # 설명을 짧게 끊음
            "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None,
            "rating": round(m.get("vote_average", 0), 1),
            "sentiment": emotion["감정"],
            "reason": emotion["공감멘트"] # 심리학자의 따뜻한 한마디
        } for m in data.get("results", [])[:5]]

# [7] 에이전트 노드 구성 (사용자 입력->감정분석(GPT)->장르결정(Rule기반)->영화추천(API)->스트리밍응답(SSE))
async def emotion_node(state: AgentState):
    return {**state, "emotion": await emotion_tool.ainvoke({"text": state["user_input"]})}

def genre_node(state: AgentState):
    mapping = {"행복": 35, "슬픔": 18, "분노": 28, "설렘": 10749, "기본": 12}
    return {**state, "genre": mapping.get(state["emotion"]["감정"], 12)}

async def recommend_node(state: AgentState):
    return {**state, "recommendations": await recommend_tool.ainvoke({"genre": state["genre"], "emotion": state["emotion"]})}

# [8] 그래프 빌드: 시작 -> 감정분석 -> 장르결정 -> 영화추천 -> 종료
def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("emotion", emotion_node)     # 감정 분석
    workflow.add_node("genre", genre_node)         # 장르 결정
    workflow.add_node("recommend", recommend_node) # 추천 생성
    
    workflow.set_entry_point("emotion")            # 시작 노드
    workflow.add_edge("emotion", "genre")
    workflow.add_edge("genre", "recommend")
    workflow.set_finish_point("recommend")         # 종료 노드
    
    return workflow.compile()

# 그래프 생성
graph = build_graph()

# [9] 웹 라우팅 설정
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index_class.html", {"request": request})

@app.get("/chat_stream")
async def chat_stream(prompt: str):
    
    async def generator():
        # LangGraph 실행 (전체 흐름 처리)
        result = await graph.ainvoke({"user_input": prompt})
        
        # SSE(Server-Sent Events) 형식으로 데이터를 실시간 전송
        yield f"data: {json.dumps({'status':'processing', 'data':result['recommendations']}, ensure_ascii=False)}\n\n"
        
        # 처리 중 상태 전달
        yield f"data: {json.dumps({'status':'complete'})}\n\n"
    
    # SSE 응답 반환    
    return StreamingResponse(generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_class:app", host="127.0.0.1", port=8000, reload=True)