
from langchain_core.prompts import ChatPromptTemplate # 사용하는 것만 import, 메모리 절약
from langchain_openai import OpenAI

import dotenv
dotenv.load_dotenv()

llm = OpenAI(temperature=0.5) 

# 구성 요소=> System Message, User(=Human) Message, AI Message
chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "너는 친절한 과학 선생님이야"), # 시스템 메세지 (system Message)
        ("user", "학생에게 {topic}을 5살 아이도 이해하기 쉽게 설명해 줘."), # 사용자 메세지 (user Message)(제한) -> 토큰(속도 향상)
        ("ai", "좋아요, 내가 학생에게 아주 잘 설명할게요") # AI 메세지 (assistant Message) : 응답할 톤 지정
])

chain = chat_prompt | llm 
print("\nChatPromptTemplate 결과:")
print(chain.invoke({"topic": "중력"}))

'''
ChatPromptTemplate 결과:
. 중력은 땅에 있는 모든 물체가 서로를 끌어당기는 힘이에요. 그래서 우리가 땅에 서있을 수 있는 거예요. 이해됐나요?
'''
