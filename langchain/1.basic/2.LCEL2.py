from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser

import dotenv
dotenv.load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini") 

prompt = ChatPromptTemplate.from_messages([
    # ("system(=role(역할))", "역할 부여할 문장")
    ("system", "너는 실력이 뛰어난 번역가야, 입력되는 영어를 아주 자연스러운 한국어로 번역해 줘."),
    ("user", "{input}")
])

# parser = StrOutputParser()
# chain = prompt | model | parser

chain = prompt | model | StrOutputParser() # 익명 객체

result = chain.invoke({"input": "Learning LangChain is fun and easy for everyone"})
print(f"번역 결과=> {result}")


'''
번역 결과=> LangChain을 배우는 것은 누구에게나 재미있고 쉬운 일입니다.
'''