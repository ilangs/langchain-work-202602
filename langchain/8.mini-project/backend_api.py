# backend_api.py
# RAG + 웹상호출 -> 데이터 요약->정보를 출력 (주제 2 유사)

from pickle import GLOBAL
import os, operator, time               # 경로, 연산자 모듈, 시간 측정용 (실행 속도)
from fastapi import FastAPI             # 비동기(=동시접속) 방식 API 서버
from typing import Annotated, TypedDict # 타입힌트 및 구조정의 (올바른 데이저 저장 목적)
from imageio.v3 import improps
from langchain_openai import ChatOpenAI, OpenAIEmbeddings       # LLM 및 임베딩
from langchain_community.document_loaders import PyPDFLoader  # pdf 파일 로딩
from langchain_community.vectorstores import FAISS              # 벡터기반 검색 DB
# 추가1 (웹검색도구 1.속도 빠름 2.정제된 데이터 반환(토큰감소))
from langchain_community.tools.tavily_search import TavilySearchResults
# 메세지 객체 종합
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain.tools import tool            # 도구 등록
from langgraph.graph import StateGraph, END # 랭그래프 workflow 구성요소
from langgraph.prebuilt import ToolNode     # 도구 실행 노드
# 추가2 (비용 체크용 콜백 함수)
from langchain_community.callbacks.manager import get_openai_callback
# OpenAI 환경 변수 
from dotenv import load_dotenv
load_dotenv()
# 추가3 (랭스미스 환경 설정)
os.environ["LANGCHAIN_TRACING_V2"] = "true"              # Langchain 추적 활성화
os.environ["LANGCHAIN_PROJECT"] = "Project_AIAgent_Dev"  # 프로젝트명 지정 (.env 동일명)

# FastAPI 객체 생성
app = FastAPI()

# 인터넷 정보는 요약 출력 + 출처 출력 필수
# 전역모델(1개) 및 벡터DB 초기화 -> 함수내에서 모델 생성 X
# 상수화 => 일단 값이 저장되면 중간에 변경이 되지 않는 변수 (=상수화변수)
GLOBAL_LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # 일관성 확보
GLOBAL_EMBEDDINGS = OpenAIEmbeddings()                       # 전역 임베딩 모델
VECTOR_DB = None                                             # 벡터 DB는 서버 시작시 초기화된다

# FAISS 벡터 DB 초기화 함수 (메모리를 절약시키는 방법 - tip)
def intialize_vector_db():
    """ 서버 시작시 PDF 문서를 읽고 FAISS 벡터 DB를 메모리에 로드 """
    global VECTOR_DB  # 함수 내부에서 전역변수를 호출할 시 선언
    index_name = "memeory_cached_index" # 저장될 인덱스 이름
    #절대 경로
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 경로
    data_dir = os.path.join(base_dir, "data")              # 데이터 폴더 경로
    target_files = ["(요약) 2025 한국 반려동물 보고서.pdf",
                    "2025_당뇨병_진료지침.pdf",
                    "반려동물_알레르기_예방관리수칙.pdf"]       # 대상 PDF 목록
    
    #1.기존 인덱스가 있으면 즉시 로드
    if os.path.exists(index_name):
        print("기존 FAISS 인덱스를 메모리에 로드합니다.")
        # 1인덱스파일명, 2임베딩객체명, 3보안옵션(신뢰한다면=True)
        VECTOR_DB = FAISS.load_local(index_name, GLOBAL_EMBEDDINGS, allow_dangerous_deserialization=True)
    #2.인덱스가 없으면pdf 파일을 읽고 새로 생성
    else:
        print("신규 PDF 인덱스를 생성합니다.(최초 1회)")
        all_docs = []
        for f in target_files:            # 3개의 파일을 읽어서 꺼내 온다
            p = os.path.join(data_dir,f)  # 3개 파일을 하나씩 꺼내어 사용
            if os.path.exists(p):         # 파일이 존재한다면
                all_docs.extend(PyPDFLoader(p).load_and_split()) # 추천->기준점(단위)을 추가하도록
        
        if all_docs:
            VECTOR_DB = FAISS.from_documents(all_docs, GLOBAL_EMBEDDINGS)  # 벡터 DB 생성
            VECTOR_DB.save_local(index_name)                               # 로컬에 저장
            print("인덱스 생성 및 메모리에 로드 완료!!!")
        else:
            print("경고: PDF 파일을 찾을 수 없습니다.")

# 서버 시작시 벡터 DB 초기화 작업 실행 (필수 실행)
intialize_vector_db()

# 도구1.로컬지식 검색 함수
@tool
def search_local_knowledge(query:str):
    """ FAISS 벡터 DB에서 관련된 문서를 검색하여 반환하는 함수 """
    if VECTOR_DB is None:                                   # 벡터 DB에 내용이 없다면
        return "로컬 지식 베이스가 로드되지 않았습니다."
    
    docs = VECTOR_DB.similarity_search(query, k=2)  # 유사도 검색 2개 반환
    # 검색 데이터와 유사한 데이터 2개를 하나씩 꺼내어(d) 페이지 단위 (본문 내용만 결합해서 반환)
    return "\n\n".join([d.page_content for d in docs])  

# 도구2.웹 검색 및 요약 함수
@tool
def search_web_integrated(query:str):
    """ Tavily 검색 결과를 요약해서 반환해주는 함수 """
    search = TavilySearchResults(k=2)  # 웹 검색 결과 2개 (정제된 데이터) 반환
    raw_data = search.run(query)       # 웹 검색 실행
    refining_prompt = f"질문 '{query}'에 대한 검색 결과에서 핵심내용만 3문장 요약: {raw_data}"
    summary = GLOBAL_LLM.invoke(refining_prompt).content   # 요약설정 | strOutputparser
    return summary

###### 기능이 더 필요하면 -> 함수 여러개 추가  ######

# 에이전트 및 그래프 설정
tools = [search_local_knowledge, search_web_integrated]  # 사용할 도구 목록
llm_with_tools = GLOBAL_LLM.bind_tools(tools)            # 도구를 바인딩한 모델

# 에이전트 상태 정의
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add] # 메세지 문자열 누적(추가 세션별로 대화 저장)

# 모델 호출 함수 정의
def call_model(state: AgentState):
    sys_msg = SystemMessage(content = "반려동물/당뇨병 전문 상담사 입니다.")
    return {"messages": [llm_with_tools.invoke([sys_msg]+state['messages'])]}

# LangGraph 워크플로우 구성
builder = StateGraph(AgentState)

# 노드 추가
builder.add_node("agent", call_model)        # 모델 호출 노드 추가
builder.add_node("action", ToolNode(tools))  # 에이전트가 호출할 도구 실행노드 등록

# 시작 지점 설정
builder.set_entry_point("agent")
builder.add_conditional_edges("agent", lambda x: "action" if x['messages'][-1].tool_calls else END)

# 엣지 추가
builder.add_edge("action", "agent") # 도구 실행후 다시 모델 호출

# 컴파일
graph_engine = builder.compile()  # 그래프 컴파일

# FastAPI 객체로 비동기 요청 처리 (=동시접속 처리)
@app.post("/ask")
async def ask_api(query: str): # {prompt} from frontend_ui.py
    """ 사용자의 질문을 받아서 LangGraph 에이전트를 실행하고 응답 반환 해주는 함수 """
    
    with get_openai_callback() as cb:  # 비용 추적 시작
        start_t = time.time()        # 시작 시간 기록
        result = graph_engine.invoke({"messages": [HumanMessage(content=query)]})  # 랭그래프 실행
        
        answer_msg = result["messages"][-1]
        answer_text = answer_msg.content if hasattr(answer_msg, "content") else str(answer_msg)
        
        return {
            "answer": answer_text,      # 최종 응답 텍스트
            "stats": {
                "latency" : round(time.time() - start_t, 2), # after-before=차이(소수점 두자리)(응답 지연시간) 
                "total_tokens": cb.total_tokens,              # 사용된 토큰수
                "total_cost": cb.total_cost,                 # 비용
                "timestamp": time.strftime("%H:%M:%S")       # 현재 시간
            }
        }
    

# 로컬 서버 실행 uvicorn backend_api:app --reload => 자동 호출 설정
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)  # FastAPI 서버 실행
