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
# print("\nPDF 로드 기반 지식창고(vector_db) 구축 완료!\n")

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

# gpt-4o-mini 모델 (기본지식(red letter) vs 전문지식 검색(RAG)(blue letter))
llm_base = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# 터미널 출력시 결과구분 => Ansi 색상코드 설정 -> 텍스트 색상변경
# \033 -> ESC(Escape) 문자를 의미 (16진수 0x1B, ASCII 제어문자)
RED = "\033[91m"    # 일반 GPT 답변을 Red 글자로 출력
BLUE = "\033[94m"   # RAG 답변을 Blue 글자로 출력
RESET = "\033[0m"   # 색상 초기화

# 테스트에 사용할 질문들을 리스트 형태로 저장
questions = [
    "삼성 메모리 카드/UFD 인증 유틸리티는 동시에 몇개의 메모리 카드나 UFD를 인식할 수 있나요?",
    "삼성 메모리 카드/UFD 인증 유틸리티는 BitLocker가 활성화된 장치나 포맷되지 않은 장치를 인증할 수 있나요?",
    "삼성 메모리 카드/UFD 인증 유틸리티에서 지원되는 운영체제(os) 버젼은 무엇입니까?"
]

# 성능 비교를 위한 반복문
for i, q in enumerate(questions, 1): # 인덱스를 1부터 시작
    print(f"\n==질문 {i}==\n")
    print("Q", q)

    # GPT 모델을 사용한 답변
    base_answer = llm_base.invoke(q)
    print(RED, "\n[일반 GPT 답변]",RESET)
    print(base_answer.content)
    
    # RAG 모델을 사용한 답변
    rag_answer = rag_chain.invoke(q)
    print(BLUE, "\n[RAG 기반 답변]",RESET)
    print(rag_answer.content)
    
'''
질문: 이 유틸리티는 동시에 몇개의 메모리 카드나 UFD(USB Flash Drive)를 인식할 수 있나요?
답변: 이 유틸리티는 동시에 최대 8개의 메모리 카드나 UFD(USB Flash Drive)를 인식할 수 있습니다.

==질문 1==

Q 삼성 메모리 카드/UFD 인증 유틸리티는 동시에 몇개의 메모리 카드나 UFD를 인식할 수 있나요?
 
[일반 GPT 답변]
삼성 메모리 카드/UFD 인증 유틸리티는 일반적으로 여러 개의 메모리 카드나 USB 플래시 드라이브(UFD)를 동시에 인식할 수 있습니다. 그러나 동시에 인식할 수 있는 개수는 사용 중인 컴퓨터의 USB 포트 수와 운영 체제의 제한 에 따라 달라질 수 있습니다. 일반적으로 USB 포트가 충분하다면 여러 개의 장치를 동시에 연결하고 인증할 수 있습니다. 정확한 개수는 유틸리티의 버전이나 사용 환경에 따라 다를 수 있으므로, 공식 문서나 지원 페이지를 참 조하는 것이 좋습니다.
 
[RAG 기반 답변]
삼성 메모리 카드/UFD 인증 유틸리티는 동시에 최대 8개의 카드를 인식할 수 있습니다.

==질문 2==

Q 삼성 메모리 카드/UFD 인증 유틸리티는 BitLocker가 활성화된 장치나 포맷되지 않은 장치를 인증할 수 있나요? 
 
[일반 GPT 답변]
삼성 메모리 카드/UFD 인증 유틸리티는 일반적으로 BitLocker가 활성화된 장치나 포맷되지 않은 장치를 인증하는 데 제한이 있을 수 있습니다. BitLocker가 활성화된 장치는 데이터가 암호화되어 있기 때문에 인증 유틸리티가 정상적으로 작동하지 않을 수 있습니다. 또한, 포맷되지 않은 장치는 파일 시스템이 없기 때문에 인증을 수행할 수 없습니다.

따라서, 인증을 원하시는 경우에는 BitLocker를 비활성화하거나 장치를 포맷한 후에 인증 유틸리티를 사용하시는 것이 좋습니다. 사용하기 전에 해당 유틸리티의 공식 문서나 지원 페이지를 참조하여 구체적인 요구 사항과 제한 사항을 확인하는 것이 좋습니다.
 
[RAG 기반 답변]
아니요, 삼성 메모리 카드/UFD 인증 유틸리티는 BitLocker가 활성화된 장치와 포맷되지 않은 장치를 인증할 수 없습니다.

==질문 3==

Q 삼성 메모리 카드/UFD 인증 유틸리티에서 지원되는 운영체제(os) 버젼은 무엇입니까?
 
[일반 GPT 답변]
삼성 메모리 카드 및 UFD(USB 플래시 드라이브) 인증 유틸리티는 일반적으로 Windows 운영 체제에서 지원됩니다. 구체적으로는 Windows 7, 8, 10, 11 등의 버전에서 사용할 수 있습니다. 그러나 최신 정보나 특정 버전의 지원 여부는 삼성 공식 웹사이트나 해당 유틸리티의 사용자 매뉴얼을 참조하는 것이 가장 정확합니다.
 
[RAG 기반 답변]
삼성 메모리 카드/UFD 인증 유틸리티에서 지원되는 운영체제는 다음과 같습니다:
- Windows 7 (32/64비트)
- Windows 8 및 8.1 (32/64비트)
- Windows 10 (32/64비트)'''




