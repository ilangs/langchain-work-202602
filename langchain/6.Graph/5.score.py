# 5.score.py

import streamlit as st  # 웹 페이지 UI 구성을 위한 메인 라이브러리
import operator  # 데이터를 누적(더하기)할 때 사용하는 연산 도구
from typing import Annotated, TypedDict  # 데이터 타입을 엄격하게 정의하는 도구
from langgraph.graph import StateGraph, END  # 랭그래프의 지도(Graph)와 종료(END) 지점
from PIL import Image, ImageDraw, ImageFont  # 이미지를 생성하고 그리는 도구
from io import BytesIO  # 이미지를 메모리 상에서 데이터로 변환할 때 사용

# --- [1단계] 공용 게시판(State) 정의 : 실행 경로(path) 기록 칸 추가 ---

class ChefState(TypedDict):
    """모든 부서가 공유하는 업무 일지입니다."""
    # Annotated와 operator.add를 사용하면 기존 대화에 새 대화가 계속 누적됨.
    messages: Annotated[list[str], operator.add]
    # [핵심] 어떤 부서를 방문했는지 '발도장'을 찍어 기록하는 리스트
    execution_path: Annotated[list[str], operator.add] 
    # 추가
    scores: Annotated[list[int], operator.add] # int (정수) => 각 부서의 점수

# --- [2단계] 각 부서(Node) 정의 : 일할 때마다 발도장(path) 찍기 ---
def planner_node(state: ChefState):
    """[기획부] 메뉴 계획을 세우고, 자신이 일했다는 증거(path)를 남깁니다."""
    return {
        "messages": ["기획부: 오늘의 업무 계획을 세웠습니다."], 
        "execution_path": ["기획부(Planner)"], # '나 여기 다녀감!' 하고 발도장 찍기
        # 추가
        "scores":[10], # 기획부의 내부 평가 점수 (임의 부여)
    }

def cook_node(state: ChefState):
    """[제작부] 요리를 완성하고, 자신이 일했다는 증거(path)를 남깁니다."""
    return {
        "messages": ["제작부: 주문하신 요리를 완성했습니다."], 
        "execution_path": ["제작부(Cook)"], # '나도 여기 다녀감!' 하고 기록 추가
        "scores":[30] # 제작부의 내부 평가 점수 (임의 부여)
    }
    
def reviewer_node(state: ChefState):
    """[검수부] 최종 확인을 하고, 마지막 발도장을 찍습니다."""
    return {
        "messages": ["검수부: 품질 검사를 마쳤습니다. 완벽합니다!"], 
        "execution_path": ["검수부(Reviewer)"], # '마지막 검수 완료!' 기록
        "scores":[20] # 검수부 내부 평가 점수 (임의 부여)
    }

# 어떤 부서가 방문했는지 화면에 출력 -> 매개변수(부서명) 반환값(O) => 입력을 받아서 처리 (계산, 저장)

# --- [3단계] 시각화 도구: 로드맵 그리기 함수 (전문가용 기술) ---
def draw_path_map(path_list, score_list): # score_list 추가
    """에이전트들이 이동한 경로 리스트를 받아 화살표 그림으로 그립니다."""
    # 도화지(800x150) color(white)
    img = Image.new('RGB', (800,150), color=(255,255,255))
    d = ImageDraw.Draw(img) # 붓
    
    # 한글이 깨지지 않게 폰트 설정
    try: font = ImageFont.truetype("./fonts/NotoSansCJKkr-Regular.otf")
    except: font = ImageFont.load_default()

    x = 50 # 첫 번째 상자를 그릴 시작 위치(가로 좌표)
    for i, node_name in enumerate(path_list):
        # 1. 부서 이름이 들어갈 네모 상자 (크기 200x100, 테두리색상 black, 테두리 굵기 2px)
        d.rectangle([x, 50, x+150, 100], outline=(0,0,0), width=2)
        # 2. 상자 안에 부서 이름 쓰기
        d.text((x+20, 65), f"{i+1}. {node_name}", font=font, fill=(0,0,0))
        
        ### [추가] 점수 출력 ###########################################################
        if i < len(score_list):
            d.text((x+20, 80), f"점수: {score_list[i]}", font=font, fill=(0,0,255))
        ##############################################################################
        
        # 3. 다음 부서가 있다면 Red 연결선 그리기
        if i < len(path_list) - 1:  # 맨 마지막 상자는 연결선 그리지 않음
            d.line([x+150, 75, x+200, 75], fill=(255,0,0), width=3)
        
        x += 200 # 다음 상자를 위해 가로 위치를 옆으로 이동
    
    # 4. 완성된 이미지를 컴퓨터가 읽을 수 있는 바이트 데이터로 변환
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue() # 그림 데이터를 반환

# --- [4단계] 랭그래프 조직도(Workflow) 구성 ---

workflow = StateGraph(ChefState) # 우리 식당의 업무 지도를 선언합니다.

# 지도에 각 부서(노드)를 배치합니다.
workflow.add_node("planner", planner_node)
workflow.add_node("cook", cook_node)
workflow.add_node("reviewer", reviewer_node)

# 부서 간 이동 경로(엣지)를 화살표로 연결합니다.
workflow.set_entry_point("planner")  # 시작은 무조건 기획부!
workflow.add_edge("planner", "cook")  # 기획 -> 조리
workflow.add_edge("cook", "reviewer") # 조리 -> 검수
workflow.add_edge("reviewer", END)    # 검수 -> 업무 종료(END)

# 설계도를 실제 실행 가능한 애플리케이션으로 컴파일합니다.
app = workflow.compile()

# --- [5단계] Streamlit 화면 출력 로직 ---

st.title("🏁 에이전트 협업 성과 점수 시스템")
st.write("멀티 에이전트들의 협업 로드맵과 평가 점수를 확인해 보세요.")

if st.button("🚀 전 부서 협업 시스템 가동"):
    # 비어있는 게시판을 들고 업무를 시작(invoke)합니다.
    result = app.invoke({"messages": [], "execution_path": [], "scores":[]})
    
    # 1. 텍스트로 된 업무 기록을 출력합니다.
    st.subheader("📝 업무 기록 일지")
    for msg in result["messages"]:
        st.info(msg)
    
    # [추가] 평가 점수
    st.subheader("🌟 최종 평가 점수")
    total_score = sum(result["scores"])
    st.success(f"최종 평가 점수: {total_score}") 

    # 2. 에이전트가 지나온 길을 그림으로 그려서 보여줍니다.
    st.divider() # 구분선
    st.subheader("🗺️ 실시간 협업 로드맵")
    # 게시판에 기록된 'execution_path'를 가져와 그림을 그립니다.
    path_img_data = draw_path_map(result["execution_path"], result["scores"])
    st.image(path_img_data) # 화면에 로드맵 표시
    
    # 3. 사용자가 로드맵을 소장할 수 있게 다운로드 버튼을 만듭니다.
    st.download_button(
        label="📂 협업 로드맵 저장하기", 
        data=path_img_data, 
        file_name="collaboration_map.png", 
        mime="image/png"
    )
    
# streamlit run 5.score.py


