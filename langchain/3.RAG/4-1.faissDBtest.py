from langchain_community.vectorstores import FAISS # 벡터 저장소
from langchain_openai import OpenAIEmbeddings # OpenAI 임베딩 모델
from langchain.text_splitter import RecursiveCharacterTextSplitter # 텍스트 분할 도구
from langchain.docstore.document import Document # 문서 객체 생성 도구

from callFunction import *

# 1. 로컬로 문자열 호출   2. 웹사이트에 접속 -> 데이터 검색

# 1. 원본문서
raw_text = """
FAISS는 Facebook AI Reasearch 에서 개발한 벡터 검색 라이브러리입니다.
대규모 벡터 데이터에서 빠른 최근접 이웃 검색을 지원합니다.
LangChain은 FAISS를 활용하여 문서 검색 및 질문 응답 시스템을 구축할 수 있습니다.
"""

# 2. 일정 길이로 문서 분할 (긴 텍스트를 작은 조각으로 나우어야 검색 효율 증가)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)

docs = text_splitter.split_documents([Document(page_content=raw_text)]) # 익명 객체
# print('\ndocs=>', docs) # 중간 점검 

# 3. 임베딩 모델 초기화 (텍스트 -> 숫자 벡터로 변환)
embeddings = OpenAIEmbeddings()
# print('\nembeddings=>', embeddings) # 중간 점검 

# 4. 문서 조각과 임베딩 모델을 합쳐서 FAISS 벡터 DB 생성
vector_db = FAISS.from_documents(docs, embeddings) # 분리된 Document를 Embedding(숫자)와 짝지어 db에 저장
# print("\nvector_db=>", vector_db) # 중간 점검 
print("지식창고(vector_db) 구축 완료!")

# 5. 사용자가 질문을 입력하면 벡터DB에서 유사문서 검색
query = "FAISS는 무엇인가요?"
search_result = vector_db.similarity_search(query, k=2) # 상위 2개의 검색 결과를 반환 (=최근접 이웃 벡터)

# 6. 검색 결과 출력
for i, result in enumerate(search_result, start=1): # start=1 => 인덱스를 1부터 시작
    print(f"\n[검색 결과 {i}] \n{result.page_content}")

'''
지식창고(vector_db) 구축 완료!

[검색 결과 1]
LangCahun은 FAISS를 활용하여 문서 검색 및 질문 응답 시스템을 구축할 수 있습니다.

[검색 결과 2]
FAISS는 Facebook AI Reasearch 에서 개발한 벡터 검색 라이브러리입니다.
대규모 벡터 데이터에서 빠른 최근접 이웃 검색을 지원합니다.
'''
