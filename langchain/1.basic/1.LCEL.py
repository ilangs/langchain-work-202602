# 모듈 불러오기 (형식) from 모듈명 import 클래스,함수-하나의 파일로 만들어서 세트(=모듈)
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate  # 대화 모듈
from langchain_core.output_parsers import StrOutputParser # 문자 형태로 출력하는 모듈

# api-key
import dotenv # 환경 변수
dotenv.load_dotenv() # 모듈명.함수명

# 1. 모델 선정
model = ChatOpenAI(model="gpt-4o-mini") # 클래스 -> 객체 생성 (1.데이터 저장, 2.메서드 호출)
# print("model=>", model) # 객체 생성 => 메모리에 공간이 잡힌다. => 주소값
'''
model=> client=<openai.resources.chat.completions.completions.Completions 
object at 0x000001A053940A40> a
'''

# 2. 프롬프트 설정 (질문 입력) -> 프롬프트 객체 생성
# 함수와 메서드 구분 (기능은 동일) (함수는 프리랜서, 매서드(=함수)는 클래스에 소속)
# 함수명(항목,,,(=매개변수명(=함수가 처리할 값)))
prompt = ChatPromptTemplate.from_template("{topic}에 대해 짧은 문장으로 설명해 줘.") #(1)
prompt = ChatPromptTemplate.from_template("랭체인에 대해 짧은 문장으로 설명해 줘.") #(2)

# 3. 출력 파서 (=양식에 맞추어 출력) (모델의 응답값중에서 문자열만 추출)
parser = StrOutputParser()  # parser 객체(=variable(변수) 생성

# 4. 체인 생성 (LCEL의 핵심) 조건을 연결 ->입력->모델->출력
chain = prompt | model | parser # 서로 연결된 정보

# 5. 응답 결과 출력
result = chain.invoke({"topic": "인공지능 에이전트"}) #(1)
print("result=>", result) #(1)
# [], {키명:전달할값} 오타 주의 =>json 형식=>데이터 전송

result = chain.invoke({}) #(2)
print("result=>", result) #(2)

'''
result=> 랭체인(LangChain)은 자연어 처리 모델과 외부 데이터 소스를 결합하여 
복잡한 애플리케이션을 구축할 수 있도록 지원하는 프레임워크입니다.
'''
