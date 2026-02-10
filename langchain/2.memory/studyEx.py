# import os # 운영체제 시스템 정보를 제어하는 모듈을 가져옵니다.
# from dotenv import load_dotenv # .env 파일에서 환경 변수를 로드하기 위한 함수를 가져옵니다.
# from langchain_openai import ChatOpenAI # OpenAI의 채팅 모델 연결 도구를 가져옵니다.
# from langchain_core.prompts import ChatPromptTemplate # 대화의 흐름을 설계하는 템플릿 도구를 가져옵니다.
# from langchain_core.output_parsers import StrOutputParser # 응답 결과를 텍스트로 깔끔하게 정리해주는 파서를 가져옵니다.

# # .env 파일에 저장된 환경 변수(API 키 등)를 시스템에 등록합니다.
# load_dotenv() 
from callFunction import *

# 1. ChatPromptTemplate 설계 (시스템 역할 정의 및 변수 설정)
# 시나리오 요구사항: 비유와 예시를 포함한 AI 선생님 역할 부여
prompt = ChatPromptTemplate.from_messages([
    ("system", """너는 기술 개념을 쉬운 비유와 예시를 섞어서 설명하는 AI 선생님이야. 
    사용자의 질문에 대해 다음 세 가지 요소를 포함하여 답변해줘:
    1.정의: 기술의 개념을 명확하게 설명
    2.이유(중요성): 왜 이 기술을 사용하는지 설명
    3.쉬운 예시: 일상생활의 비유를 들어 초보자도 이해하기 쉽게 설명"""), 
    ("user", "{question}") # 사용자가 입력하는 질문이 들어갈 자리입니다.
])

# 2. ChatOpenAI 모델 설정
# 시나리오 요구사항: gpt-4o-mini 모델 사용 및 temperature 0.7 설정
llm = ChatOpenAI(
    model="gpt-4o-mini", # 사용할 모델명을 지정
    temperature=0.7 # 답변의 창의성을 높여 비유를 풍부하게 
)

# 3. StrOutputParser 설정
# AI가 반환하는 데이터 중 텍스트 본문만 추출하도록 설정
parser = StrOutputParser()

# 4. LCEL 문법으로 파이프라인(체인) 구성
# 데이터의 흐름: 프롬프트 구성 -> 모델 전달 -> 결과 파싱
chain = prompt | llm | parser

# 5. 실행 및 결과 출력
# 시나리오에 있는 "REST API" 질문으로 테스트를 수행합니다.
if __name__ == "__main__": # 스크립트가 직접 실행될 때만 작동합니다.
    input_data = {"question": "REST API란?"} # 입력할 질문 데이터를 정의합니다.
    response = chain.invoke(input_data) # 체인을 실행하여 AI 답변을 생성합니다.
    
    print("-" * 50) # 구분선 출력
    print(f"질문: {input_data['question']}") # 입력된 질문 확인
    print("-" * 50) # 구분선 출력
    print(response) # AI의 최종 답변 출력

'''
--------------------------------------------------
질문: REST API란?
--------------------------------------------------
1. **정의**: REST API는 "Representational State Transfer Application Programming Interface"의 약자 로, 웹에서 데이터를 주고받기 위한 규칙과 형식을 정의한 것입니다. REST는 주로 HTTP 프로토콜을 이용해 클라이언트와 서버 간의 상호작용을 가능하게 하며, 특정한 형식(주로 JSON 또는 XML)으로 데이터를 전송합니다.

2. **이유(중요성)**: REST API는 시스템 간의 통신을 표준화하여 개발자들이 쉽게 데이터를 주고받을 수 있도록 해줍니다. 이는 다양한 플랫폼과 언어에서 호환성을 높여주고, 유지보수나 확장성을 용이하게 합니다. 즉, REST API를 사용하면 서로 다른 시스템 간에도 데이터를 쉽게 교환할 수 있어, 웹 서비스나 모바 일 앱 등에서 매우 중요한 역할을 합니다.

3. **쉬운 예시**: REST API를 생각할 때, 레스토랑의 메뉴와 주문 시스템에 비유할 수 있습니다. 레스토 랑의 메뉴는 고객이 어떤 음식을 주문할 수 있는지를 보여줍니다. 고객이 음식을 주문하면, 웨이터가 주방에 그 주문을 전달하고, 주방에서 요리를 만들어 다시 웨이터를 통해 고객에게 제공합니다. 여기서 메뉴가 REST API의 역할을 하고, 고객이 주문하는 과정이 클라이언트와 서버 간의 데이터 요청과 응답을 나타냅 니다. 따라서 REST API는 서로 다른 시스템(주방과 고객)이 소통할 수 있게 해주는 메뉴와 같은 존재라고 할 수 있습니다.
'''