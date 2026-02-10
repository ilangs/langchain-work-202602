from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import dotenv
dotenv.load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini",temperature=0.5) 

# ~ 찾아서 보여줘 => 찾는 양이 많아서 tokens max limited => 요약해 줘. or 300자 이내로 알려 줘.
prompt = ChatPromptTemplate.from_template(
    "다음 한국어 문장을 영어로 번역하는데, 반드시 10단어 이내로 간결하게 답해 줘: \n문장: {korean_text}"
)

chain = prompt | model | StrOutputParser()

user_input = "오늘 날씨가 너무 좋아서 근처 공원에 산책을 가고 싶다."
res = chain.invoke({"korean_text": user_input})

print(f"입력: {user_input}\n결과: {res}")


'''
입력: 오늘 날씨가 너무 좋아서 근처 공원에 산책을 가고 싶다.
결과: The weather is nice; I want to walk in the park.
'''
