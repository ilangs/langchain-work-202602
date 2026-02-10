from langchain_community.vectorstores import FAISS # 벡터 저장소
from langchain_openai import OpenAIEmbeddings # OpenAI 임베딩 모델
from langchain.text_splitter import RecursiveCharacterTextSplitter # 텍스트 분할 도구
from langchain.docstore.document import Document # 문서 객체 생성 도구

from callFunction import *

# 추가 ###########################################################################################
from langchain_community.document_loaders import PyPDFLoader # pdf 파일 불러오는 클래스
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough # langchain의 LECL 문법
from langchain_core.prompts import ChatPromptTemplate # llm에게 전달할 질문형식을 정의 프로프트 템플릿
#################################################################################################

# 1. PDF 파일 로드
loader = PyPDFLoader("C:/workAI/work/LangChain/3.RAG/data/Samsung_Card_Manual_Korean_1.3.pdf")
pages = loader.load() # List[documents] 객체로 변환
# print('\ntype(pages)=>', type(pages)) # 중간 점검

# 2. 일정 길이로 문서 분할 (긴 텍스트를 작은 조각으로 나우어야 검색 효율 증가)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

docs = text_splitter.split_documents(pages) # 익명 객체
# print('\ndocs=>', docs) # 중간 점검 

# 3. 임베딩 모델 초기화 (텍스트 -> 숫자 벡터로 변환)
embeddings = OpenAIEmbeddings()
# print('\nembeddings=>', embeddings) # 중간 점검 

# 4. 문서 조각과 임베딩 모델을 합쳐서 FAISS 벡터 DB 생성
vector_db = FAISS.from_documents(docs, embeddings) # 분리된 Document를 Embedding(숫자)와 짝지어 db에 저장
# print("\nvector_db=>", vector_db) # 중간 점검 
print("\nPDF 로드 기반 지식창고(vector_db) 구축 완료!\n")

############### 검색기(retriever) 객체 생성 ######################
retriever = vector_db.as_retriever(search_Kwargs={"k":3}) # "k":3 => 상위 3개의 유사 검색 결과를 반환

# 5. 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_template("""
    당신은 삼정전자 메모리카드 매뉴얼에 대한 전문 어시스턴트 입니다.
    다음의 참고 문서를 바탕으로 질문에 정확하게 답변 해 주세요.

    [참고 문서]
    {context}

    [질문]
    {question}
    
    한글로 간결하고 정확하게 답변 해 주세요.
""") 

rag_chain = (
    # 입력을 question으로 받아서 retriever에게 전달
    {"context": retriever, "question": RunnablePassthrough()} 
    | prompt
    | ChatOpenAI(model="gpt-4o-mini", temperature=0) # 창의성(x)
)

# 6. 검색기(retriever)에게 질문 전달
query = "이 유틸리티는 동시에 몇개의 메모리 카드나 UFD(USB Flash Drive)를 인식할 수 있나요?" # 예시
answer = rag_chain.invoke(query)

# 7. 결과 출력
print(f"질문: {query}")
print(f"답변: {answer.content}") # 원하는 문자열만 검색


'''
PDF 로드 기반 지식창고(vector_db) 구축 완료!

질문: 이 유틸리티는 동시에 몇개의 메모리 카드나 UFD(USB Flash Drive)를 인식할 수 있나요?
답변: 이 유틸리티는 동시에 최대 8개의 메모리 카드나 UFD(USB Flash Drive)를 인식할 수 있습니다.
'''
