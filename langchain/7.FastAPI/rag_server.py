# rag_server.py (FastAPI 기반 RAG 서버)
#1.모듈 설치
### 추가 #########################################################
from fastapi import FastAPI     # FastAPI 서버 프레임워크
from pydantic import BaseModel  # 요청 데이터 모델 정의용
from langchain.prompts import ChatPromptTemplate  # 프롬프트 설계
#################################################################
from langchain_community.vectorstores import FAISS  # 벡터 저장소
from langchain_openai import OpenAIEmbeddings, ChatOpenAI  # OpenAI 임베딩 모델 + LLM
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 문서 분할
from langchain.docstore.document import Document # 문서 객체 생성

import requests # 웹페이지 요청을 보내주는 라이브러리
from bs4 import BeautifulSoup # HTML을 파싱(=분석)하여 텍스트를 추출하는 라이브러리

#2.환경변수 로딩
from dotenv import load_dotenv
load_dotenv()

#3.FastAPI 앱 생성
app = FastAPI() # 앱 객체 생성

#4.전역객체 초기화=> rag_server.py의 어느 위치에 있어도 항상 호출하여 사용하는 객체
# vs 지역객체 => 특정 함수내에서 사용하는 변수()

#임베딩 모델 초기화 (텍스트 -> 숫자 벡터로 변환)
embeddings = OpenAIEmbeddings()
print('embeddings=>', embeddings) # 중간 점검 

#LLM 모델 생성
llm = ChatOpenAI(
    model = "gpt-4o-mini",  # 토큰 부족 방지
    temperature = 0         # 일관성 있는 답변
)

#5.데이터 로딩 및 벡터 DB 생성

def build_vector_db():
    
    url = "https://ko.wikipedia.org/wiki/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5" #웹크롤링

    #웹사이트(URL)에 HTTP 요청으로 보내서 페이지 내용을 가져오기
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; MyRAGBot/1.0; +https://example.com/bot)"}
    ) 
    print('response=>', response) #중간점검 확인 코딩(=디버깅 코딩)
    soup = BeautifulSoup(response.text, "html.parser") # HTML을 파싱(=분석)하여 텍스트를 추출
    raw_text = soup.get_text()
    print('raw_text=>', raw_text) 

    # 긴 문자열을 작은 조각으로 분할하여 검색효율 증가
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50) #500자단위 50자겹침
    docs = splitter.split_documents([Document(page_content=raw_text)])
    print('docs=>', docs) # 중간 점검 

    #문서 조각과 임베딩 모델을 합쳐서 FAISS 벡터 DB 생성
    vector_db = FAISS.from_documents(docs, embeddings)
    print("vector_db=>", vector_db) # 중간 점검 
    print("웹 크롤링 기반 지식창고(vector_db) 구축 완료!")
    
    return vector_db

#서버 시작시 벡터DB 생성
vector_db = build_vector_db()

#6.요청 모델 정의
class QuestionReuest(BaseModel):
    question: str  #클라이언트에서 보낼 질문

#7.사용자가 질문을 입력하면 벡터DB에서 유사문서 검색
@app.post("/ask")
def ask_question(request: QuestionReuest):
    #질문 추출
    query = request.question
    print('query=>', query) # 중간 점검
    
    #벡터 유사도 검색
    results = vector_db.similarity_search(query, k=3) #상위 3개의 결과 반환 (=최근접 인접벡터)
    print('result=>', results) # 중간 점검
    
    #검색결과 출력 (유사검색된 여러 페이지들을 document객체단위로 쪼개서 page_content 단위로 결합)
    context = "\n\n".join([doc.page_content for doc in results]) #전처리
    print('context=>', context) # 중간 점검
    
    #프롬프트 구성
    prompt = ChatPromptTemplate.from_template("""
        당신은 AI 전문가입니다.
        반드시 아래 문서를 참고하고, 요약하여 답변해 주세요.
        문서에 없는 내용은 추측하지 마세요.
        
        문서:
        {context}
        
        질문:
        {question}        
    """)
    
    #체인 생성
    chain = prompt | llm
    
    #LLM 호출
    response = chain.invoke({
        "context": context,
        "question":query        
    })
    
    #json 반환
    return {"answer": response.content}

# uvicorn rag_server:app --reload
# http://localhost:8000/docs