# txt.pdf 파일 불러오기
from langchain_community.document_loaders import PyPDFLoader

import os

# 1. 경로를 지정하여 읽을 준비
# 1) 절대 경로 (\ 대신에 / 사용)
# loader = PyPDFLoader("C:/workAI/work/LangChain/3.RAG/data/Samsung_Card_Manual_Korean_1.3.pdf")

# 2) 상대 경로
# os.path.abspath(__file__) => 현재 파일(__file__)의 전체 경로를 반환 해 주는 함수
# os.path.dirname( ) => 그 전체 경로 중에서 폴더 경로만 반환 해주는 메서드
current_dir = os.path.dirname(os.path.abspath(__file__)) # __file__ : 파이썬 파일의 경로
# +data\삼성 파일 경로
pdf_path = os.path.join(current_dir, "data","Samsung_Card_Manual_Korean_1.3.pdf")

print(f"현재 파이썬이 위치한 곳 (절대 경로) : {os.getcwd()}") #c:\workAI\work

loader = PyPDFLoader(pdf_path)

#2. 페이지별로 문서 로드
pages = loader.load() 

print("자료형=>", type(pages))
print(f"총페이지 수=>: {len(pages)}쪽")

print(f"1페이지 미리보기=> {pages[0].page_content[:500]}") # 슬라이싱 500자 출력 -> 문법 예시 [1:3] [:2]