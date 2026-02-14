# LangGraphWork.py 배달 부서 추가

import streamlit as st  
import operator  
from typing import Annotated, TypedDict  
from langgraph.graph import StateGraph, END  
from PIL import Image, ImageDraw, ImageFont  
from io import BytesIO  

# --- [1단계] 공용 게시판(State) 정의  ---
class ChefState(TypedDict):
    """모든 부서가 공유하는 업무 일지입니다."""
    messages: Annotated[list[str], operator.add]
    execution_path: Annotated[list[str], operator.add] 
    scores: Annotated[list[int], operator.add] 
    errors: Annotated[list[str], operator.add] 

# --- [2단계] 각 부서(Node) 정의  ---
def planner_node(state: ChefState):
    """[기획부] 메뉴 계획을 세우고, 자신이 일했다는 증거(path)를 남깁니다."""
    return {
        "messages": ["🧠 기획부: 오늘의 업무 계획을 세웠습니다."], 
        "execution_path": ["기획부(Planner)"], 
        "scores":[10], 
        "errors":[]    
    }

def cook_node(state: ChefState):
    """[제작부] 요리를 완성하고, 자신이 일했다는 증거(path)를 남깁니다."""
    return {
        "messages": ["🛠️ 제작부: 주문하신 요리를 완성했습니다."], 
        "execution_path": ["제작부(Cook)"], 
        "scores":[30], 
        "errors":[]    
    }

def marketing_node(state: ChefState):
    """[홍보부] 메뉴를 홍보하는 부서입니다."""
    return {
        "messages": ["📣 홍보부: 오늘의 메뉴를 SNS에 홍보했습니다."],
        "execution_path": ["홍보부(Marketing)"], 
        "scores":[15],   
        "errors":[]    
    }
    
def reviewer_node(state: ChefState):
    """[검수부] 최종 확인을 하고, 마지막 발도장을 찍습니다."""
    return {
        "messages": ["🔍 검수부: 품질 검사를 마쳤습니다. 완벽합니다!"], 
        "execution_path": ["검수부(Reviewer)"], 
        "scores":[20], 
        "errors":[]    
    }

###### 배달(Delivery) 부서 추가 ################################################
def delivery_node(state: ChefState):
    """[배달부] 메뉴을 배달하고, 배달 기록을 남깁니다."""
    return {
        "messages": ["🚚 배달부: 오늘의 메뉴을 배달하겠습니다."], 
        "execution_path": ["배달부(Delivery)"], 
        "scores":[25], 
        "errors":[]    
    }
##############################################################################

def error_handler_node(state: ChefState):
    """[에러 처리부] 에러가 발생했을 때 처리하는 부서"""
    return {
       "messages": ["🚨 시스템 알림: 에러 발생! 작업 중단합니다."],
       "execution_path": ["에러 처리(Error Handler)"], 
       "scores":[0], 
       "errors":[]
    }

# --- [3단계] 시각화 로드맵 그리기  ---
def draw_path_map(path_list, score_list, error_list): 
    """ 부서 경로와 점수를 함께 시각화 (에러 메세지도 박스 안에 표시) """
    
    img = Image.new('RGB', (900, 150), color=(255,255,255))
    d = ImageDraw.Draw(img) 
    
    try: font = ImageFont.truetype("./fonts/NotoSansCJKkr-Regular.otf", 15)
    except: font = ImageFont.load_default()

    x = 10 # 첫 번째 상자 시작 위치
    for i, node_name in enumerate(path_list):
        # 1.부서 이름이 들어갈 네모 상자 
        d.rectangle([x, 50, x+150, 120], outline=(0,0,0), width=2)
        # 2.상자 안에 부서 이름 쓰기
        d.text((x+10, 60), f"{i+1}.{node_name}", font=font, fill=(0,0,0))
        # 3.평가점수 출력
        if i < len(score_list):
            d.text((x+20, 80), f"점수: {score_list[i]}", font=font, fill=(0,0,255))
        # 4.에러 출력 (에러가 있을 경우에만)
        if i < len(error_list) and error_list[i]:
            d.text((x+20, 100), f"에러: {error_list[i]}", font=font, fill=(255,0,0))
        # 5.다음 부서에 Red 연결선
        if i < len(path_list) - 1: # 맨 마지막 상자는 연결선 그리지 않음
            d.line([x+150, 80, x+180, 80], fill=(255,0,0), width=3)
        
        x += 180 # 다음 상자를 위해 가로 위치를 옆으로 이동
    
    # 6. 완성된 이미지를 컴퓨터가 읽을 수 있는 바이트 데이터로 변환
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue() 

# --- [4단계] 랭그래프 조직도(Workflow) 구성 ---
workflow = StateGraph(ChefState) 

# 지도에 각 부서(노드)를 배치
workflow.add_node("planner", planner_node)
workflow.add_node("cook", cook_node)
workflow.add_node("marketing", marketing_node)
#########################################################################
workflow.add_node("delivery", delivery_node) # [배달부] 요리 배달 부서
#########################################################################
workflow.add_node("reviewer", reviewer_node)
workflow.add_node("error_handler", error_handler_node)

# 부서 간 이동 경로를 연결
workflow.set_entry_point("planner")        # 시작은 기획부!
workflow.add_edge("planner", "cook")       # 기획 -> 조리
workflow.add_edge("planner", "marketing")  # 기획 -> 홍보

workflow.add_conditional_edges("cook", lambda state: "error_handler" if state["errors"] else "reviewer")

workflow.add_edge("marketing", "reviewer")  # 홍보 -> 검수
###### 배달(Delivery) 부서 추가 ###########################################
workflow.add_edge("reviewer", "delivery")   # 검수 -> 배달
workflow.add_edge("delivery", END)          # 배달 -> 종료 (정상 상황)
#########################################################################
workflow.add_edge("error_handler", END)     # 에러 처리 -> 종료 (이상 상황)

app = workflow.compile()

# --- [5단계] Streamlit 화면 출력 로직 ---
st.title("🏁 병렬 처리 협업 시스템")
st.write("멀티 에이전트들의 협업 과정을 로드맵으로 확인해 보세요.")

if st.button("🚀 전 부서 협업 시스템 가동"):
    
    result = app.invoke({"messages": [], "execution_path": [], "scores":[], "errors":[]})
    
    # 1. 업무 기록 출력
    st.subheader("📝 업무 기록 일지")
    for msg in result["messages"]:
        st.info(msg)
    
    st.divider()
    st.subheader("🗺️ 에이전트 협업 구조")
    
    # 2. 평가 점수
    st.subheader("🌟 최종 평가 점수")
    total_score = sum(result["scores"])
    st.success(f"최종 평가 점수: {total_score}") 

    # 3. 에러 정보
    if any(err and err.strip() for err in result["errors"]): 
        st.subheader("🚨 에러 로그")
        actual_errors = [e for e in result["errors"] if e] 
        for err in actual_errors:
            st.error(err)

    # 4. 에이전트 로드맵 표시
    st.divider() # 구분선
    st.subheader("🗺️ 병렬 협업 로드맵")
    path_img_data = draw_path_map(result["execution_path"], result["scores"], result["errors"])
    st.image(path_img_data) 
    
    #5. 로드맵 다운로드 버튼
    st.download_button(
        label="📂 협업 로드맵 저장하기", 
        data=path_img_data, 
        file_name="collaboration_map.png", 
        mime="image/png"
    )
    
# streamlit run LangGraphWork.py
