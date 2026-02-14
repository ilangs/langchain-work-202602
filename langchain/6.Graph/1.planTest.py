# 1.planTest.py 어떤 요리 기획?

import streamlit as st
from typing import Annotated, TypedDict     # 데이터 타입 정의 도구 = 모든 부서의 공용 게시판
import operator                             # 공용 게시판 메세지들을 차곡차곡 누적하여 저장 + 연산
from langgraph.graph import StateGraph, END # 부서들간의 흐름도 (시작->부서이동->종료)


# --- [1단계] 공용 게시판(State) 만들기 ---
# 모든 부서가 같이 보고 내용을 적는 공유 문서 (회사) -> 데이터 저장, 저장 확인
# 상속(속성과 메서드를 상속받음=>소유권 이전) => 정확하게 원하는 데이터 저장? 확인 가능
# TypedDict => 1.타입 명확성, 2.타입검사, 3.상태(State)데이터의 일관성 보장
class ChefState(TypedDict): # class 사용자 정의 자료형(=클래스 이름)(상속받을 부모 클레스명)
    # 속성값 or 메서드명      # 클래스를 작성하는 이유 -> 객체를 생성하기 위해 -> 1.데이터 저장, 2.메서드 호출
    messages: Annotated[list[str], operator.add] # messages 변수에 문자형의 데이터를 차곡차곡 쌓아서 저장

# --- [2단계] 각 부서(Node)의 업무 정의하기 ---

def planning_department(state: ChefState): # 변수명:자료형(=어떤 데이터의 종류(float)와 범위(소수점)를 지정)
    """[기획부서] 사용자의 요청을 보고 무엇을 할지 계획을 세웁니다."""
    st.write("🔍 **[기획부]** : 음, 손님이 케이크를 원하시네, 레시피를 찾아야겠어.")
    # 게시판에 기획 완료 메시지를 추가합니다.
    return {"messages": ["기획부: 고구마 케이크 레시피 찾기 계획 수립!"]}

def cooking_department(state: ChefState):
    """[제작부서] 기획서가 넘어오면 실제로 요리(실행)를 합니다."""
    st.write("🛠️ **[제작부]** : 기획서 확인 완료! 지금 바로 케이크를 만듭니다.")
    # 게시판에 제작 완료 메시지를 추가합니다.
    return {"messages": ["제작부: 달콤한 고구마 케이크 완성!"]}

# --- [3단계] 부서 배치 및 결재 라인(Graph) 연결 ---

# 1. 우리 식당의 업무 지도(Graph)를 그리기 시작합니다.

workflow = StateGraph(ChefState)

# 2. 식당에 부서들을 배치합니다 (Node 추가(=부서이름, 함수명))
workflow.add_node("planner", planning_department)  # 기획부 배치
workflow.add_node("cook", cooking_department)      # 제작부 배치

# 3. 부서 간의 이동 경로를 설정합니다 (Edge 연결)
workflow.set_entry_point("planner")   # 모든 일은 '기획부'에서 시작해!
workflow.add_edge("planner", "cook")  # 기획이 끝나면 바로 '제작부'로 가! (1.시작부서, 2.다음부서)
workflow.add_edge("cook", END)        # 제작이 끝나면 모든 업무 종료!

# 4. 설계도를 실제 실행 가능한 앱으로 만듭니다.
app = workflow.compile()

# --- [4단계] 실제로 시스템 가동하기 ---

st.title("🏗️ 분업 시스템 (LangGraph)")

if st.button("협업 시스템 가동!"):
    # 초기 게시판 내용을 비워서 업무를 시작합니다.
    initial_state = {"messages": []}
    
    # 지도를 따라 부서별로 일이 진행됩니다.
    final_outcome = app.invoke(initial_state)
    
    st.divider()
    st.subheader("📋 공용 게시판 최종 기록")
    # 모든 부서가 기록한 내용을 화면에 뿌려줍니다.
    for msg in final_outcome["messages"]:
        st.write(msg)


# streamlit run 1.planTest.py
#
# 🏗️ 분업 시스템 (LangGraph)
#
# 🔍 [기획부] : 음, 손님이 케이크를 원하시네, 레시피를 찾아야겠어.
#
# 🛠️ [제작부] : 기획서 확인 완료! 지금 바로 케이크를 만듭니다.
#
# 📋 공용 게시판 최종 기록
#
# 기획부: 고구마 케이크 레시피 찾기 계획 수립!
#
# 제작부: 달콤한 고구마 케이크 완성!