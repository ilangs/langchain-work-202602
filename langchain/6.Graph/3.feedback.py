# 3.feedback.py 기획 -> 제작 -> 검수 FeedBack

import streamlit as st
from typing import Annotated, TypedDict     # 데이터 타입 정의 도구 = 모든 부서의 공용 게시판
import random                               # 검수 통과 여부를 무작위로 결정하기 위해서 사용
import operator                             # 공용 게시판 메세지들을 차곡차곡 누적하여 저장 + 연산
from langgraph.graph import StateGraph, END # 부서들간의 흐름도 (시작->부서이동->종료)


# --- [1단계] 공용 게시판(State) 만들기 ---
# 모든 부서가 같이 보고 내용을 적는 공유 문서 (회사) -> 데이터 저장, 저장 확인
# 상속(속성과 메서드를 상속받음=>소유권 이전) => 정확하게 원하는 데이터 저장? 확인 가능
# TypedDict => 1.타입 명확성, 2.타입검사, 3.상태(State)데이터의 일관성 보장
class ChefState(TypedDict): # class 사용자 정의 자료형(=클래스 이름)(상속받을 부모 클레스명)
    """ 부서원들이 공유하는 업무 일지입니다."""
    # 속성값 or 메서드명      # 클래스를 작성하는 이유 -> 객체를 생성하기 위해 -> 1.데이터 저장, 2.메서드 호출
    messages: Annotated[list[str], operator.add] # messages 변수에 문자형의 데이터를 차곡차곡 쌓아서 저장
    # 요리를 몇번 다시 시고했는지 숫가로 기록하여 무한루프를 방지 합니다.
    attempts: int


# --- [2단계] 각 부서(Node)의 업무 정의하기 ---

def planning_department(state: ChefState): # 변수명:자료형(=어떤 데이터의 종류(float)와 범위(소수점)를 지정)
    """[기획부] 메뉴를 정하고 업무를 시작합니다."""
    st.write("🧠 **[기획부]** : 오늘의 메뉴는 '매운 떡볶이' 입니다.")
    # 게시판에 기획 완료를 적고, 시도 횟수를 0으로 초기화하여 전달합니다.
    return {"messages": ["기획: 매운 떡볶이 기획 완료"], "attempts":0}

def cooking_department(state: ChefState):
    """[제작부] 기획서나 지배인의 피드백을 보고 요리를 만듭니다."""
    # 현재 게시판에 적힌 시도 횟수를 가져와서 1을 더합니다.
    current_attempt = state.get("attempts", 0) + 1   # 매개변수(객체)
    st.write(f"🛠️ **[제작부]** : {current_attempt}번째 떡볶이를 열심히 만들고 있습니다!")
    # 요리한 결과 메시지와 업데이트된 시도 횟수를 게시판에 적습니다.
    return {"messages": [f"제작: {current_attempt}차 떡볶이 조리 완료"], "attempts": current_attempt}

def reviewer_department(state: ChefState):
    """[검수부] 완성된 요리를 먹어보고 품질을 평가합니다."""
    st.write("🔍 **[검수부]** : 지배인이 맛을 보는 중입니다...")
    # 검수했다는 사실만 게시판에 기록합니다. (통과 여부는 다음 단계에서 결정)
    return {"messages": ["검수: 지배인이 시식함!!"]}


# ##### [3단계] 길을 결정하는 신호등 함수 (중요!!) #######################################

def should_continue(state: ChefState):
    """지배인의 판단에 따라 다음 부서로 보낼지, 일을 끝낼지 결정합니다."""
    
    # Random 함수 이용 True(합격)/False(불합격) 
    quality_pass = random.choice([True, False])
    
    # [무한 루프 방지] 3번 이상이면 통과
    if state["attempts"] >= 3:
        st.warning("⚠️ (지배인) : 시간이 너무 지체됐군. 그냥 이대로 손님에게 드려!")
        return "finish" # 'finish'라는 신호를 보냅니다.
    
    # 품질 검사를 통과하는 경우
    if quality_pass:
        st.success("✨ (지배인) : 맛이 훌륭합니다! 퇴근하세요.")
        return "finish" # 'finish' 신호 발생
    # 품질 검사에 실패하는 경우
    else:
        st.error("❌ (지배인) : 너무 짜요! 다시 만들어 오세요!")
        return "retry" # 'retry' 신호를 보내서 다시 요리하게 합니다.
    
####################################################################################

# --- [4단계] 부서 배치 및 지능형 지도 구성 ---

# 지도를 그릴 도화지(StateGraph)를 준비합니다.
workflow = StateGraph(ChefState)

# 각 부서를 지도 위에 올립니다.
workflow.add_node("planner", planning_department) # 기획 부서
workflow.add_node("cook", cooking_department)     # 조리 부서
workflow.add_node("reviewer", reviewer_department)# 검수 부서

# 기본 화살표를 연결합니다 (직진 코스)
workflow.set_entry_point("planner")    # 시작은 기획부!
workflow.add_edge("planner", "cook")    # 기획 -> 조리
workflow.add_edge("cook", "reviewer")   # 조리 -> 검수


##### [핵심] 검수부(reviewer) 조건에 따라 분기 #######################################

workflow.add_conditional_edges(
    "reviewer",            # 출발지: 검수부
    should_continue,       # 판단 함수: 지배인의 입맛
    {
        "retry": "cook",   # 함수가 'retry'를 반환하면 조리부(cook)로 복귀!
        "finish": END      # 함수가 'finish'를 반환하면 업무 종료(END)!
    }
)
###################################################################################

# 설계도를 실제 실행 가능한 앱으로 만든다.
app = workflow.compile()

# --- [5단계] 웹 화면 실행 ---

st.title("🔄 조건부 이동 (Loop & Feedback)")
st.write("기획부 -> 제작부 -> 검수부로 이어지는 '멀티 에이전트'의 흐름을 확인하세요.")

if st.button("협업 주방 가동!"):
    # 게시판이 비어있는 상태로 일을 시작합니다.
    initial_state = {"messages": [], "attempts": 0}
    # 지도를 따라 부서별로 업무 진행
    final_result = app.invoke(initial_state) 
    
    st.divider()
    st.subheader("📋 최종 업무 히스토리")
    # 게시판에 쌓인 메시지를 하나씩 화면에 출력합니다.
    for i, msg in enumerate(final_result["messages"]):
        st.write(f"{i+1}단계: {msg}")


# streamlit run 3.feedback.py

# 🔄 조건부 이동 (Loop & Feedback)
#
# 🧠 [기획부] : 오늘의 메뉴는 '매운 떡볶이' 입니다.
#
# 🛠️ [제작부] : 1번째 떡볶이를 열심히 만들고 있습니다!
#
# 🔍 *[검수부] : 지배인이 맛을 보는 중입니다...
#
# ❌ (지배인) : 너무 짜요! 다시 만들어 오세요!
#
# 🛠️ [제작부] : 2번째 떡볶이를 열심히 만들고 있습니다!
#
# 🔍 [검수부] : 지배인이 맛을 보는 중입니다...
#
# ❌ (지배인) : 너무 짜요! 다시 만들어 오세요!
#
# 🛠️ [제작부] : 3번째 떡볶이를 열심히 만들고 있습니다!
#
# 🔍 [검수부] : 지배인이 맛을 보는 중입니다...
#
# ⚠️ (지배인) : 시간이 너무 지체됐군. 그냥 이대로 손님에게 드려!
#
#
# 📋 최종 업무 히스토리
#
# 기획: 매운 떡볶이 기획 완료
# 제작: 1차 떡볶이 조리 완료
# 검수: 지배인이 시식함
# 제작: 2차 떡볶이 조리 완료
# 검수: 지배인이 시식함
# 제작: 3차 떡볶이 조리 완료
# 검수: 지배인이 시식함
