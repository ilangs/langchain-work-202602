
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

chat_history = "사용자: 내 이름은 '테스트김'이야.\nAI: 반가워요, 테스트김 님!" # 미리 언급한 정보를 저장

prompt = ChatPromptTemplate.from_template("이전 대화:{history}\n질문: {input}")
chain = prompt | model | StrOutputParser()

# 과거 대화내역을 한꺼번에 전송
res = chain.invoke({"history": chat_history,"input": "내 이름이 뭔지 알아?"})
print(f"수동 메모리 응답: {res}")

'''
수동 메모리 응답: 네, 당신의 이름은 '테스트김'입니다!
'''
