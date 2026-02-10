from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate 

import dotenv
dotenv.load_dotenv()

# parameter 변경 
# temperature = 0~1 사이 (0 = 정확성(창의성 없음), 1에 가까울수록 창의성 증가)
model = ChatOpenAI(model="gpt-4o-mini",temperature=0.9) # 생성자(=객체가 생성될 때 자동으로 호출되는 함수) 

prompt = ChatPromptTemplate.from_template(
    "다음 뉴스 내용을 바탕으로 사람들의 클릭을 유도하는 '낚시성' 헤드라인 3개를 만들어 줘:{content}"
)

chain = prompt | model

news_content = "애플이 새로운 AI 기능을 탑재한 아이폰 18을 내년에 출시한다고 발표했습니다." 
# request(요청), response(응답)
res = chain.invoke({"content": news_content})  # "news.content"(x)=>문자열
print(res.content) # 응답 객체명.특정키명=>값을 불러온다. 
# 객체 생성 목적 -> 1.데이터 저장, 2.메서드 호출 
# 객체명.속성명(get)  객체명.속성명=값
print("===============================================================================")
print(res)

'''
1. "애플의 아이폰 18, 내년에 등장! 인공지능이 바꿀 미래의 스마트폰?!"
2. "아이폰 18의 AI 혁명! 애플이 공개한 놀라운 기능들!"
3. "애플이 준비한 아이폰 18, 당신의 삶을 완전히 변화시킬 AI 탑재!"
===============================================================================
content='1. "애플의 아이폰 18, 내년에 등장! 인공지능이 바꿀 미래의 스마트폰?!"\n2. "아이폰 18의 AI 혁명! 애플이 공개한 놀라운 기능들!"\n3. "애플이 준비한 아이폰 18, 당신의 삶을 완전히 변화시킬 AI 탑재!"' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 78, 'prompt_tokens': 61, 'total_tokens': 139, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_f4ae844694', 'id': 'chatcmpl-D5ncogUUWR5D7ilZ75GhFRrIXpgAs', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='run--019c2c99-4a2e-7300-9dab-42287a72d568-0' usage_metadata={'input_tokens': 61, 'output_tokens': 78, 'total_tokens': 139, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
'''