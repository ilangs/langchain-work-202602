# main.py파일 수정
# 1.LLM 호출은 가능한 1번만 호출토록 제한 (토큰 사용량 감축)
# 2.좀 더 다양한 감정의 사용자를 이해하고 추천할 수 있도록 페르소나 조절
# 3.추천한 영화의 이유를 간략하게 출력이 되게 설계

# (추가 수정) 각 영화별로 고유한 추천 사유를 출력하도록 수정
# 1.Backend (main.py): LLM에게 '추천 사유'를 미리 만들지 않고, 영화 목록을 가져온 후에 LLM을
#   한 번 더 호출하여 5편의 영화에 대한 개별적인 사유를 생성 (LLM 호출은 최적화 방법으로 2회로 제한)
# 2.Frontend (index.html): 공통사유 영역 대신 Backend에서 보내주는 개별 사유(reason)를 각 카드에 표시

import os, json, asyncio, httpx
from typing import TypedDict, List
from dotenv import load_dotenv
from pathlib import Path

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware  # CORS 추가

# [1] 설정 로드
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# [2] FastAPI 설정
app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR/"static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR/"templates"))

# CORS 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# [3] AI 모델 (온도를 약간 높여 공감 능력 향상)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# [4] 데이터 통로 정의 (AgentState)
class AgentState(TypedDict):
    user_input: str
    analysis: dict        # 1차 분석: 감정, 장르 코드, 공감 멘트
    movies: list          # TMDB에서 가져온 생 영화 데이터
    recommendations: list # 최종 가공된 추천 리스트 (개별 사유 포함)

# [5] 통합 분석 노드 (1차 LLM 호출)
async def analysis_node(state: AgentState):
    """사용자의 입력을 분석하여 기본적인 감정, 장르 코드, 공감 멘트를 한 번에 추출합니다."""
    prompt = f"""
    당신은 영화를 통해 마음을 치유하는 '시네마 테라피스트'입니다. 
    사용자의 상황과 감정을 깊이 읽고, 그에 맞는 영화 장르를 선정하세요.

    [장르 코드 참조]
    - 행복: 35(코미디) / 슬픔: 18(드라마) / 분노: 28(액션) / 설렘: 10749(로맨스) / 
      긴장: 53(스릴러) / 공허: 12(모험) / 위로: 16(애니메이션) / 기본: 12

    반드시 아래 JSON 형식으로만 답변하세요:
    {{
        "emotion": "분석된 감정 키워드",
        "genre_code": 123,
        "empathy_message": "사용자에게 전하는 따뜻한 세로 읽기 공감 멘트 (최대 2줄, 문장이 끝나는 마침표 뒤에서는 줄바꿈)"
    }}
    
    입력: "{state['user_input']}"
    """
    
    res = await llm.ainvoke(prompt)
    try:
        content = res.content.replace("```json", "").replace("```", "").strip()
        analysis = json.loads(content)
    except:
        analysis = {
            "emotion": "기본", "genre_code": 12, 
            "empathy_message": "당신의 곁에\n편안한 영화 한 편\n두고 갑니다."
        }
    # analysis만 업데이트하여 넘김
    return {**state, "analysis": analysis}

# [6] 영화 목록 가져오기 노드 (TMDB API 호출)
async def get_movies_node(state: AgentState):
    """분석된 장르 코드를 바탕으로 영화 목록을 가져옵니다."""
    genre = state["analysis"]["genre_code"]
    
    async with httpx.AsyncClient() as client:
        res = await client.get(
            "https://api.themoviedb.org/3/discover/movie",
            params={
                "api_key": TMDB_API_KEY,
                "language": "ko-KR",
                "with_genres": genre,
                "vote_average.gte": 7.5,      # 좀 더 엄선된 명작
                "sort_by": "popularity.desc"
            }
        )
        data = res.json()
        # 생 영화 데이터만 업데이트하여 넘김
        return {**state, "movies": data.get("results", [])[:5]}

# [7] 개별 사유 생성 노드 (2차 LLM 호출 - 핵심 수정 사항)
async def create_reasons_node(state: AgentState):
    """가져온 영화 목록과 사용자의 감정을 기반으로 각 영화별 개별 사유를 생성합니다."""
    
    # 영화 정보 문자열로 구성 (LLM에게 전달용)
    movie_info_str = "\n".join([f"- 제목: {m['title']}, 줄거리: {m.get('overview', '')[:50]}..." for m in state["movies"]])
    
    prompt = f"""
    당신은 30년 경력의 심리학 박사이자 시네마 테라피스트입니다.
    사용자는 현재 '{state['analysis']['emotion']}' 상태입니다.
    아래 5편의 영화에 대해 사용자의 현재 감정을 치유할 수 있는 **심리학적 관점의 간략하고 고유한 추천 사유**를 작성해 주세요.

    [영화 목록]
    {movie_info_str}

    반드시 아래 JSON 형식으로만 답변하세요 (각 영화 제목을 키로 하고, 사유를 값으로 하는 딕셔너리 형태):
    {{
        "영화제목1": "사용자의 '{state['analysis']['emotion']}' 감정을 이렇게 어루만져 줄 것입니다.",
        "영화제목2": "이 영화 속 인물의 여정이 당신의 지친 마음에 새로운 용기를 줍니다.",
        ...
    }}
    """
    
    res = await llm.ainvoke(prompt)
    try:
        content = res.content.replace("```json", "").replace("```", "").strip()
        reasons_dict = json.loads(content)
    except:
        reasons_dict = {} # 기본값은 빈 딕셔너리

    # 최종 추천 리스트 구성 (영화 정보 + 개별 사유 조합)
    recs = []
    for m in state["movies"]:
        title = m["title"]
        # LLM이 생성한 사유가 있으면 사용, 없으면 기본 메시지
        reason = reasons_dict.get(title, f"{title}은(는) 당신의 기분을 전환해 줄 것입니다.")
        
        recs.append({
            "title": title,
            "desc": m.get("overview", "설명이 제공되지 않는 영화입니다.")[:60] + "...",
            "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None,
            "rating": round(m.get("vote_average", 0), 1),
            "sentiment": state["analysis"]["emotion"],
            "reason": reason  # 영화별 고유 사유 적용!
        })
            
    return {**state, "recommendations": recs}

# [8] 그래프 빌드 (노드 순서 및 데이터 흐름 수정)
def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("analysis", analysis_node)          # 1. 감정/장르 분석 (LLM1)
    workflow.add_node("get_movies", get_movies_node)    # 2. 영화 목록 가져오기 (API)
    workflow.add_node("create_reasons", create_reasons_node) # 3. 개별 사유 생성 (LLM2)
    
    workflow.set_entry_point("analysis")
    workflow.add_edge("analysis", "get_movies")
    workflow.add_edge("get_movies", "create_reasons")
    workflow.add_edge("create_reasons", END)
    
    return workflow.compile()

graph = build_graph()

# [9] 라우팅 (chat_stream은 동일)
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat_stream")
async def chat_stream(prompt: str):
    async def generator():
        # LangGraph 실행 (전체 흐름 처리)
        result = await graph.ainvoke({"user_input": prompt})
        
        # 처리 중 상태 및 데이터 전달
        yield f"data: {json.dumps({'status':'processing', 'data':result['recommendations'], 'message': result['analysis']['empathy_message']}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'status':'complete'})}\n\n"
    
    return StreamingResponse(generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)