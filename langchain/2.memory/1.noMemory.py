# ctrl+a(전체 블럭 지정)

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("{input}")
chain = prompt | model | StrOutputParser()

# 첫 번째 질문
print(f"질문 1: 내 이름은 '테스트김'이야. / 응답: {chain.invoke({'input': '내 이름은 테스트김이야.'})}")
# 두 번째 질문 (기억 못함)
print(f"질문 2: 내 이름이 뭔지 알아? / 응답: {chain.invoke({'input': '내 이름이 뭔지 알아?'})}")


'''
질문 1: 내 이름은 '테스트김'이야. / 응답: 안녕하세요, 테스트김님! 어떻게 도와드릴까요?
질문 2: 내 이름이 뭔지 알아? / 응답: 죄송하지만, 당신의 이름을 알 수 없습니다. 어떤 이름을 원하시거나 다른 질문이 있으시면 말씀해 주세요!
'''
