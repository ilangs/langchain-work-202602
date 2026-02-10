from callFunction import *
# LangChain 커뮤니티 모듈에서 대화 기록 관리 클래스 불러오기
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import OpenAI

# LLM 초기화
llm = OpenAI(temperature=0.5)

# 대화 기록 객체 생성
history = ChatMessageHistory()

# 기능 => 함수
# 1. 매개변수 x, 반환값 x => 단순 반복적인 업무 실행
# 2. 매개변수 o, 반환값 x => 데이터 저장 목적, 계산 목적
# 3. 매개변수 o, 반환값 o => 계산 목적 
def show_history(): # def 함수명() or (매개변수명,,):
    # 함수 => work function() 협업=>함수들이 순서에 따라서 호출-> 실행(Agent)
    ''' 현재까지의 대화기록을 보기 좋게 출력 '''
    print("\n=== 대화 기록 ===\n")
    # for 출력변수 in 출력대상자(=객체):
    for msg in history.messages: # 저장된 데이터 출력
        role = "사용자" if msg.type == "human" else "AI" # 삼항 연산자
        print(f"{role}: {msg.content}") # 역할과 메세지 내용을 출력
    print("\n================\n")
    
           
def main(): # caller function (업무를 지시하는 함수) => 직원명(매개변수명)로 호출
    print("대화를 시작합니다. 'exit' 입력시 종료")
    while True:
        user_input = input("\n>>>")
        if user_input.lower() == "exit":
            print("프로그램을 종료합니다.")
            break
        # 사용자 메세지 기록
        history.add_user_message(user_input)
        # LLM 응답 생성
        ai_response = llm.invoke(user_input)
        # AI 메세지 기록
        history.add_ai_message(ai_response)
        # 응답 출력
        print(f"AI: {ai_response}")
        
        # 대화 기록 출력
        show_history()

# 함수가 없는 경우 => 그냥 실행 OK
# 함수가 있는 경우 => 모듈 형태로 많이 사용한다.
# -> 1. 현재 파일에서 실행시키는 경우  2. 외부에서 모듈로 사용하는 경우

# 1. 현재 파일내에서 main()함수를 부른다면 main()함수를 실행
if __name__ == "__main__": 
    main()
    print("__name__:", __name__) # exit 입력하면 __name__: __main__ 출력
    
    # 2. main()함수를 모듈로 사용하는 경우
    # from chatMessagesHistory import main
    # main()
    
""" 
>>>부산의 유명한 관광지 소개해 줘
AI: 

부산에는 많은 관광지가 있지만 그 중에서도 유명한 관광지를 소개해드리겠습니다.

1. 해운대해수욕장
부산을 대표하는 해수욕장으로 국내외에서 많은 관광객이 찾는 곳입니다. 넓은 백사장과 시원한 바다를 즐길 수 있으며 주변에는 맛있는 음식점과 다양한 놀이시설도 있어서 가족 여행에도 좋습니다.

2. 광안리해수욕장
해운대해수욕장과 인접해 있는 광안리해수욕장은 해운대보다는 조용하고 여유로운 분위기를 느낄 수 있습니다. 해변을 따라 늘어선 레스토랑과 카페에서

=== 대화 기록 ===

사용자: 부산의 유명한 관광지 소개해 줘
AI:

부산에는 많은 관광지가 있지만 그 중에서도 유명한 관광지를 소개해드리겠습니다.

1. 해운대해수욕장
부산을 대표하는 해수욕장으로 국내외에서 많은 관광객이 찾는 곳입니다. 넓은 백사장과 시원한 바다를 즐길 수 있으며 주변에는 맛있는 음식점과 다양한 놀이시설도 있어서 가족 여행에도 좋습니다.

2. 광안리해수욕장
해운대해수욕장과 인접해 있는 광안리해수욕장은 해운대보다는 조용하고 여유로운 분위기를 느낄 수 있습니다. 해변을 따라 늘어선 레스토랑과 카페에서

================

>>>exit
프로그램을 종료합니다.
__name__: __main__

"""