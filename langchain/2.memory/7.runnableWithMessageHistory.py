# 1.
from callFunction import *  # *: 모듈내에 있는 모든 요소 (클래스, 함수, ...)

# 2. 새로운 클레스 로딩
from langchain_core.chat_history import InMemoryChatMessageHistory # 세션별 대화 저장
from langchain_core.runnables import RunnableWithMessageHistory # 연속 대화 시뮬레이션
from langchain_core.messages import HumanMessage # 사용자 메시지 객체 (=UserMessage)

# 3. OpenAI 채팅 모델 객체 생성
model = ChatOpenAI(model="gpt-4o-mini")  

# 4. 세션 저장소 생성
store = {} # 세션별 대화기록을 저장할 딕셔너리(초기화)

# 5. 세션별 history를 반환하는 함수 (매개변수(=함수가 해야할 일) o, 반환값 o) = 직원
def get_session_history(session_id:str): # 매개변수명:자료형(=문자인지, 숫자인지, 객체인지 알려줌)
    if session_id not in store: # 세션이 없다면 새로 만들어서 삽입
        store[session_id] = InMemoryChatMessageHistory() # 새로운 메모리 객체 생성 -> 데이터 저장 목적
    return store[session_id]    # 해당 세션의 메모리 객체를 반환

# 6. 채팅 체인 생성 (RunnableWithMessageHistory 적용)
with_message_history = RunnableWithMessageHistory(
    model, # 실행할 모델
    get_session_history # 세션별 대화 기록을 반환하는 함수 
)

# 7. 실행 요청 목록 정의
requests = [
    {"seesion_id": "abc2", "message": "안녕? 난 테스트김 입니다."},
    {"seesion_id": "abc2", "message": "내 이름이 무엇입니까?"},
    {"seesion_id": "abc3", "message": "내 이름이 무엇입니까?"},
    {"seesion_id": "abc2", "message": "아까 우리가 무슨 얘기했지요?"},
]

# 8. 일반 invoke 실행 (for문 사용)
print("\n===== 일반 invoke 실행 =====\n")

for req in requests:
    
    # 세션 ID 설정
    # configurable => 랭체인 내부적으로 실행 시점에 동적으로 바뀔 수 있다라고 지정해 주는 옵션 (예약어)
    # session_id => 누가 대화하고 있는지를 구분하는 방번호
    # req["session_id"] => 사용자로 부터 들어온 요청(request)에서 실제 세션id값을 추출하여 할당
    config = {"configurable": {"session_id": req["seesion_id"]}}
    
    # 모델 실행 (HumanMessage 객체 전달)
    response = with_message_history.invoke(
        HumanMessage(content=req["message"]), # 세션별 대화내용 전달
        config # 세션별 id값을 전달
    ) 
    
    # 세션 정보와 함께 출력
    print(f"sesion_id={req['seesion_id']}") # 세션 id
    print(f"User: {req['message']}")        # 사용자 메시지
    print(f"AI: {response.content}")        # AI 답변
    print("-"*50)

# 9️. stream 실행 예시
print("\n===== stream 실행 (abc2 유지) =====\n")

stream_config = {"configurable": {"session_id": "abc2"}}

print("[Session: abc2]")
print("User: 내가 어느 나라 사람인지 맞춰보고, 그 나라의 문화에 대해 말해 봐")
print("AI: ", end="", flush=True) # 실시간으로 바로바로 출력 (flush=True)

# 스트리밍 방식으로 모델 응답 출력 (한글자씩 출력)  
for chunk in with_message_history.stream(
    HumanMessage(content="내가 어느 나라 사람인지 맞춰보고, 그 나라의 문화에 대해 말해 봐"),
    stream_config
):
    print(chunk.content, end="", flush=True)

print("\n"+"-"*50)

# 10. 현재 세션 메모리 상태 확인
print("\n===== 현재 세션 메모리 상태 확인 =====\n")

# 이중 for문 사용
for session_id, history in store.items(): # {키, 값~}
    print(f"sesion_id: {session_id}") # 세션별로 구분
    for msg in history.messages:
        print(f" - {msg.type}: {msg.content}") # 메시지 타입(human/ai)과 내용 출력
    print("-"*50)

'''

'''