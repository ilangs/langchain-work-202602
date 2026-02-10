# PromptTemplate, ChatPromptTemplate 차이점

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import OpenAI

import dotenv
dotenv.load_dotenv()

llm = OpenAI(temperature=0.5) 

# ~ 찾아서 보여줘 => 찾는 양이 많아서 tokens max limited => 요약해 줘. or 300자 이내로 알려 줘.

prompt = PromptTemplate(
    input_variables=["topic"], # 입력 변수
    template="다음 주제에 대해 간단히 설명해 줘: {topic}"
)

chain1 = prompt | llm 
print("promptTemplate 결과:")
print(chain1.invoke({"topic": "인공지능"}))
print('======================================================================')

# CatOpenAI 객체 별도 선언 model
chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "너는 친절한 상담사야"), # 시스템 메세지 (system Message)
        ("user", "다음 주제에 대해 5살 어린이도 알기 쉽게 설명해줘: {topic}"), # 사용자 메세지 (user Message)
])

chain2 = chat_prompt | llm 
print("\nChatPromptTemplate 결과:")
print(chain2.invoke({"topic": "인공지능"}))

'''
promptTemplate 결과:
인공지능은 컴퓨터 프로그램이 인간의 지능을 모방하거나 대체하기 위해 만들어진 기술이다. 이를 위해 다양한 분야 의 학문과 기술들이 결합되어 사용되며, 기계 학습, 자연어 처리, 패턴 인식 등의 기술을 활용하여 문제를 해결하고 의사결정을 내리는 능력을 갖춘 시스템을 만들어낸다. 인공지능은 이미 우리 생활 속에서 다양한 분야에서 활용되고 있으며, 더 나은 미래를 위해 계속 발전하고 있다.
======================================================================

ChatPromptTemplate 결과:
인공지능은 컴퓨터가 사람처럼 학습하고 추론할 수 있는 능력을 갖춘 기술이야. 예를 들면, 우리가 얼굴을 보고 그 사람이 누구인지 알아낼 수 있는 것처럼, 인공지능도 데이터를 분석하고 패턴을 파악하여 미리 학습된 정보를 바탕으로 판단하고 결론을 내릴 수 있어. 이렇게 학습된 인공지능은 많은 분야에서 우리 일상을 편리하게 만들어주고 있어.
'''