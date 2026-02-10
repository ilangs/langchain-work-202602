from callFunction import *  # *: 모듈내에 있는 모든 요소 (클래스, 함수, ...)

# ===== 1️.공통 import 추가 =====
from langchain_core.prompts import MessagesPlaceholder  # 여러 메시지를 통째로 삽입하는 자리표시자
from langchain_core.messages import HumanMessage, AIMessage  # 메시지 객체 타입

# ===== 2️.LLM 모델 생성 =====
model = ChatOpenAI(model="gpt-4o-mini")  # OpenAI 채팅 모델 객체 생성


# ===== 3️. 프롬프트 설계 =====
# 함수의 매개변수명은 변경
prompt = ChatPromptTemplate.from_messages([  # 채팅 프롬프트 구조 정의
    ("system", "당신은 사용자의 이전 대화를 기억하는 전문 비서입니다."),  # 시스템 역할 정의
    MessagesPlaceholder(variable_name="chat_history"),  
    # ↑ chat_history라는 변수에 들어오는 메시지 리스트를
    #   이 위치에 그대로 삽입하겠다는 의미
    ("user", "{input}")  # 현재 사용자 입력 자리
])


# ===== 4️. 체인 구성 =====
chain = prompt | model | StrOutputParser()
# prompt → model → 문자열 출력 형태로 변환

# ===== 5️. 대화 기록 저장 리스트 =====
chat_history = []  # HumanMessage, AIMessage 객체를 계속 누적

print("대화를 시작합니다. 종료하려면 exit 입력")

# ===== 6. 대화 반복 루프 =====
while True:  # 들여쓰기 => 제어문과 함수, 클래스 작성할 때 자동으로 들여쓰기 필요
    user_input = input("\n사용자: ")  # 사용자 입력 받기

    # "exit" 객체명.호출할 메서드명() => 파이썬에서는 모든 것이 거의 객체 (문자열도 객체)
    if user_input.lower() == "exit":  # 종료 조건
        break

    # ===== 7️. LLM 호출 =====
    response = chain.invoke({
        "input": user_input,          # 현재 질문
        "chat_history": chat_history  # 이전 대화 전체 전달
    })

    print("AI:", response)

    # ===== 8️.대화 기록 누적 =====
    # 사용자가 불어보는 질문과 AI 응답을 구분하여 저장 => 호출할 때도 구분 호출
    
    # Hu = HumanMessages(content=user_input)
    # chat_history.append(Hu)
    chat_history.append(HumanMessage(content=user_input)) # 사용자 질문 저장, 축약형(익명 객체로 저장)
    
    # AI = AIMessages(content=response
    # chat_history.append(AI))
    chat_history.append(AIMessage(content=response))  # AI 응답 저장, 축약형 (익명 객체로 저장)
    
'''
대화를 시작합니다. 종료하려면 exit 입력

사용자: 내 이름은 테스트김 입니다.
AI: 안녕하세요, 테스트김님! 어떻게 도와드릴까요?

사용자: 오늘 날씨는 어때? 만약에 날씨가 좋으면 놀러가기 좋은 장소좀 추천좀해줘
AI: 오늘의 날씨에 대한 정보는 실시간으로 제공할 수는 없지만, 날씨가 좋다면 다양한 놀러가기 좋은 장소 를 추천할 수 있습니다. 예를 들어:

1. **공원**: 가까운 공원에서 피크닉이나 산책을 즐길 수 있습니다.
2. **해변**: 바다나 호숫가로 가서 수영이나 일광욕을 할 수 있습니다.
3. **산**: 등산이나 트레킹을 하며 자연을 만끽할 수 있습니다.
4. **자전거 도로**: 자전거를 타고 시원한 바람을 느끼며 즐거운 시간을 보낼 수 있습니다.
5. **카페**: 야외 테라스가 있는 카페에서 음료를 즐기며 여유를 부릴 수 있습니다.

어떤 장소가 가장 끌리시나요?

사용자: 내이름이 어떻게 돼?
AI: 당신의 이름은 테스트김입니다! 다른 질문이 있으신가요?

사용자: 아까 내가 물어본것이 뭐지?
AI: 아까 테스트김님께서 오늘 날씨에 대해서 물어보셨고, 날씨가 좋으면 놀러가기 좋은 장소를 추천해 달라고 하셨습니다. 추가로 궁금한 점이 있으신가요?

사용자: exit
'''
