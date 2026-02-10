# txt.pdf 파일 불러오기
from callFunction import *
from langchain_community.document_loaders import PyPDFLoader

# 1. 경로를 지정하여 읽을 준비
# 2) 파이썬의 상대경로를 통해서 불러오는 방법
import os
print(f"현재 파이썬이 위치한 곳 : {os.getcwd()}") # C:\workAI\work

os.chdir("C:/workAI/work/LangChain/3.RAG") # -> \를 /로 변경
loader = PyPDFLoader("./data/Samsung_Card_Manual_Korean_1.3.pdf")
print(f"현재 파이썬이 위치한 곳 : {os.getcwd()}") # C:\workAI\work\LangChain\3.RAG


# 2. 페이지별로 문서 로드
pages = loader.load() 

print("자료형=>", type(pages))
print(f"총페이지 수=>: {len(pages)}쪽")

print(f"1페이지 미리보기=> {pages[0].page_content[:500]}") # 슬라이싱 500자 출력 -> 문법 예시 [1:3] [:2]

# 기능2
from langchain_text_splitters import RecursiveCharacterTextSplitter # 텍스트 분할 도구

# chunk_size=500 (문자토막 문자수 500자), chunk_overlap=50 (문맥 연결 위해 겹치는 문자수 50자)
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50) # 0~500,450~1000,1050~1200

# 문서를 청크 단위로 분할
docs = splitter.split_documents(pages)
print(f"분할된 청크의 수=>: {len(docs)}개") # 9개


# 기능3 -> 문자열를 숫자로 바꾸는 작업 (=벡터화)

from langchain_openai import OpenAIEmbeddings # 문자열을 숫자로 바꿔주는 클래스

embeddings = OpenAIEmbeddings() # OoenAI 임베딩 모델 생성 => 메서드 필요

vector = embeddings.embed_query("인공지능 에이전트란 무엇인가요?")
print(f"변환된 숫자 벡터 길이=> {len(vector)}") # 변환된 숫자 벡터 길이 => 1536