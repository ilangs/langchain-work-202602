from langchain_community.vectorstores import FAISS # 벡터 저장소
from langchain_openai import OpenAIEmbeddings # OpenAI 임베딩 모델
from langchain.text_splitter import RecursiveCharacterTextSplitter # 텍스트 분할 도구
from langchain.docstore.document import Document # 문서 객체 생성 도구

from callFunction import *

# 추가 ########################################################################
import requests # 웹페이지 요청을 보내주는 라이브러리
from bs4 import BeautifulSoup # HTML을 파싱(=분석)하여 텍스트를 추출하는 라이브러리
##############################################################################

# 1. 로컬로 문자열 호출   2. 웹사이트에 접속 -> 데이터 검색

# # 1. 원본문서
# raw_text = """
# FAISS는 Facebook AI Reasearch 에서 개발한 벡터 검색 라이브러리입니다.
# 대규모 벡터 데이터에서 빠른 최근접 이웃 검색을 지원합니다.
# LangChain은 FAISS를 활용하여 문서 검색 및 질문 응답 시스템을 구축할 수 있습니다.
# """

# 2. 웹사이트 접속 데이터 추출 ###############################################################
url = "https://ko.wikipedia.org/wiki/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5" # 웹크롤링 기법

# 해당 웹사이트(URL)에 HTTP 요청으로 보네서 페이지 내용을 가져오기
response = requests.get(url,
    headers={"User-Agent": "Mozilla/5.0 (compatible; MyRAGBot/1.0; +https://example.com/bot)"}
) 

soup = BeautifulSoup(response.text, "html.parser") # HTML을 파싱(=분석)하여 텍스트를 추출
raw_text = soup.get_text()
# print('\nraw_text=>', raw_text) # 중간 점검
###########################################################################################

# 2. 일정 길이로 문서 분할 (긴 텍스트를 작은 조각으로 나우어야 검색 효율 증가)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

docs = text_splitter.split_documents([Document(page_content=raw_text)]) # 익명 객체
# print('\ndocs=>', docs) # 중간 점검 

# 3. 임베딩 모델 초기화 (텍스트 -> 숫자 벡터로 변환)
embeddings = OpenAIEmbeddings()
# print('\nembeddings=>', embeddings) # 중간 점검 

# 4. 문서 조각과 임베딩 모델을 합쳐서 FAISS 벡터 DB 생성
vector_db = FAISS.from_documents(docs, embeddings) # 분리된 Document를 Embedding(숫자)와 짝지어 db에 저장
# print("\nvector_db=>", vector_db) # 중간 점검 
print("웹 크롤링 기반 지식창고(vector_db) 구축 완료!")

# 5. 사용자가 질문을 입력하면 벡터DB에서 유사문서 검색
query = "인공지능이란 무엇인가요?"
search_result = vector_db.similarity_search(query, k=2) # 상위 2개의 검색 결과를 반환 (=최근접 이웃 벡터)

# 6. 검색 결과 출력
for i, result in enumerate(search_result, start=1): # start=1 => 인덱스를 1부터 시작
    print(f"\n[검색 결과 {i}] \n{result.page_content[:300]}") # 앞부분 300자만 출력

'''
웹 크롤링 기반 지식창고(vector_db) 구축 완료!

[검색 결과 1]
어떤 철학자들은 우리가 약한 인공지능을 가능한 것으로 받아들인다면, 강한 인공지능 역시 받아들여야 한다고 주장한다. 지능은 외견상 보이는 것을 가리키는 것이지 진정한 실체가 아니라는 약한 인공지능의 입장은 많은 비판을 받고 있다. 그러나 이에 반하는 손쉬운 예를 사이먼 블랙번의 철학 입문서 "생각"에서 찾을 수 있다. 블랙번은 당신이 지능적으로 보이지만, 그 지능이 실존하는가에 대해서 말할 수 있는 방법이 없다고 지적한다. 그는 우리는 단지 믿음 또는 신념 위에서 그것을 다룰 뿐이라고 이야기한다.
강한 인공지능을 지지하는 사람들은

[검색 결과 2]
약인공지능
 이 부분의 본문은 약한 인공지능입니다.
약인공지능(weak AI)은 사진에서 물체를 찾거나 소리를 듣고 상황을 파악하는 것과 같이 기존에 인간은 쉽게 해결할 수 있으나 컴퓨터로 처리하기에는 어려웠던 각종 문제를 컴퓨터로 수행하게 만드는데 중점을 두고 있다. 한참 막연한 인간 지능을 목표로 하기보다는 더 현실적으로 실용적인 목표를 가지고 개발되고 있는 인공지능이라고 할 수 있 으며, 일반적인 지능을 가진 무언가라기보다는 특정한 문제를 해결하는 도구로써 활용된다.
강인공지능 (AGI)
'''


