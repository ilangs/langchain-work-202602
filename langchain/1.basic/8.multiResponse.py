
from langchain_core.prompts import ChatPromptTemplate # 사용하는 것만 import, 메모리 효율성
from langchain_openai import OpenAI

# 라이브러리 (자주 사용되는 함수,클래스,속성) = Module (모듈)
# import dotenv # 환경변수 => import 모듈명 -> 내부에 있는 다른 함수도 불러올 수 있다.
# dotenv.load_dotenv() # 모듈명.불러올 함수형태로 사용

from dotenv import load_dotenv
load_dotenv()
# 모듈을 직접 만들어서 불러와서 사용 가능 (=사용자 정의 모듈 작성)

llm = OpenAI(temperature=0.5) 

# System Message: 모델의 성격,역할,규칙을 정의 
# User Message(=Human Message): 실제 입력값을 전달하는 부분 
# AI Message: 모델의 응답 톤이나 기본 답변 스타일을 지정

# 구성 요소=> System Message, User(=Human) Message, AI Message
chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 친절한 여행 가이드입니다."), # 시스템 메세지 (system Message)
        ("user", "나는 {city}에 여행을 가고 싶어요."), # 첫번째 사용자 메세지 (user Message)(제한) -> 토큰(속도 향상)
        ("ai", "좋아요, 내가 여행계획을 잘 설계해서 도와 드릴게요."), # AI 메세지 (assistant Message) : 응답할 톤 지정
        ("user", "그 도시의 유명한 맛집과 날씨도 같이 알려 주세요.") # 두번째 사용자 메세지 (user Message)
])

chain = chat_prompt | llm 
print(chain.invoke({"city": "파리"}))

'''
AI: 파리에서 유명한 맛집으로는 루브르 박물관 근처에 위치한 라 디포르트 레스토랑이 있어요. 그리고 파리는 4계절 모두 아름다운 도시이지만, 여름에는 매우 더워지기 때문에 가을이나 봄에 방문하는 것이 좋아요. 가볍고 시원한 옷을 준비하는 것을 추천해드릴게요.
'''
