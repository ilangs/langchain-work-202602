# gpt-4o-mini -> 이미지를 읽어 들여서 처리하는 방법

import base64 # 이미지를 텍스트로 변환하는 모듈
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

# 1. 이미지 파일을 읽어서 인코딩하는 경우
def encode_image(image_path):
    with open(image_path, "rb") as f: # with open(1.불러올 경로 포함 파일명, 2.불러오는 모드)
        return base64.b64encode(f.read()).decode("utf-8") 
    
image_base64 = encode_image("C:/workAI/work/LangChain/4.Multi-Modal-RAG/images/local_stitch_terrarosa.jpg") # 뉴스 사진

# 2. 멀티모달 메세지 구성
message = HumanMessage(content=[
    {"type": "text", "text": "이 사진을 기자처럼 자세히 설명 해 주세요."},
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64, {image_base64}"}}
])

# 3. 실행
response = model.invoke([message])
print(f"사진 분석 결과: {response.content}")
   
