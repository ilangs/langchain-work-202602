import streamlit as st  # 웹 페이지 UI 구성을 위한 기본 라이브러리
import operator  # 상태 데이터 병합 시 누적(더하기) 연산에 사용
from typing import Annotated, TypedDict  # 타입 엄격 정의 도구
from langgraph.graph import StateGraph, END  # 랭그래프 워크플로우 구조 및 종료 지점
from PIL import Image, ImageDraw, ImageFont  # 이미지 생성 및 그림 그리기 도구
from io import BytesIO  # 메모리 내 이미지 바이트 변환용 도구

# --- [1단계] 공용 상태(State) 정의 ---
class ChefState(TypedDict):
    """각 부서가 공유하는 업무 상태 구조입니다."""
    messages: Annotated[list[str], operator.add]        # 메시지 기록 누적
    execution_path: Annotated[list[str], operator.add]  # 경로 기록 누적 (어떤 부서를 거쳤는지)
    scores: Annotated[list[int], operator.add]          # 각 부서마다 기록한 점수 누적
    errors: Annotated[list[str], operator.add]          # 에러 발생 시 기록 누적

# --- [2단계] 각 부서 노드 정의 ---
def planner_node(state: ChefState):
    """기획부: 업무 계획 수립"""
    return {
        "messages": ["기획부: 오늘의 업무 계획을 세웠습니다."],
        "execution_path": ["기획부(Planner)"],  # 경로에 기획부 추가
        "scores": [10],   # 기획부 점수 부여
        "errors": []      # 에러 없음
    }

def cook_node(state: ChefState):
    """제작부: 요리 완성 담당"""
    return {
        "messages": ["제작부: 주문하신 요리를 완성했습니다."],
        "execution_path": ["제작부(Cook)"],  # 경로에 제작부 추가
        "scores": [30],   # 제작부 점수
        "errors": []      # 정상 처리 시 빈 리스트 반환
    }

def marketing_node(state: ChefState):
    """홍보부: 메뉴 SNS 홍보 작업"""
    return {
        "messages": ["홍보부: 오늘의 메뉴를 SNS에 홍보했습니다."],
        "execution_path": ["홍보부(Marketing)"],  # 홍보부 경로에 추가
        "scores": [15],   # 홍보부 점수 등록
        "errors": []      # 에러 없음
    }

def reviewer_node(state: ChefState):
    """검수부: 품질 검사 수행"""
    return {
        "messages": ["검수부: 품질 검사를 마쳤습니다. 완벽합니다!"],
        "execution_path": ["검수부(Reviewer)"],  # 검수부 경로
        "scores": [20],   # 검수부 점수
        "errors": []      # 에러 없음
    }
############검수부##########################################
def delivery_node(state: ChefState):
    """배달부: 고객에게 배달 완료"""
    return {
        "messages": ["배달부: 고객님께 배달을 완료했습니다."],
        "execution_path": ["배달부(Delivery)"],  # 배달부 경로
        "scores": [25],   # 배달부 점수
        "errors": []      # 에러 없음
    }
#############################################################
def error_handler_node(state: ChefState):
    """에러 처리부: 오류 발생 시 작업 중단 및 처리"""
    return {
        "messages": ["⚠️ 시스템 알림: 에러가 발생하여 작업을 중단합니다."],
        "execution_path": ["에러 처리(Error Handler)"],  # 에러 처리부 경로
        "scores": [0],    # 에러 처리 점수는 0으로 처리
        "errors": state["errors"]  # 현재 상태 에러 전달
    }

# --- [3단계] 시각화 함수 ---
def draw_path_map(path_list, score_list):
    """
    협업 부서 경로와 점수를 시각화합니다.
    좌우에 동일한 여백을 주고 노드 수에 따라 이미지 폭 동적으로 조절합니다.
    """
    x_start = 50  # 좌측 여백 크기 (px)
    node_width = 150  # 각 부서 노드 사각형의 가로 길이 (px)
    node_height = 50  # 노드 사각형 높이 (px)
    node_gap = 50     # 노드 간 연결선 포함 간격 (px)

    # 전체 이미지 너비 계산 = 좌측여백 + (노드 개수 * 노드 폭) + (노드 간격 * (노드 개수-1)) + 우측 여백(=좌측 여백)
    total_width = x_start + len(path_list) * node_width + (len(path_list) - 1) * node_gap + x_start

    # 이미지 새로 생성 (배경 흰색)
    img = Image.new('RGB', (total_width, 200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)  # 그리기 객체 생성

    try:
        # 한글 폰트 불러오기, 없으면 기본 폰트 사용
        font = ImageFont.truetype("./fonts/NotoSansCJKkr-Regular.otf", 15)
    except:
        font = ImageFont.load_default()

    x = x_start  # 첫 노드 시작 위치 설정 (여백 후 시작)
    y_top = 50   # 사각형 위쪽 y 위치
    y_bottom = y_top + node_height  # 사각형 아래쪽 y 위치 계산

    for i, node_name in enumerate(path_list):
        # 노드 사각형 그리기
        d.rectangle([x, y_top, x + node_width, y_bottom], outline=(0, 0, 0), width=2)
        # 부서명 텍스트 출력 (좌측 상단 약간 내부 위치)
        d.text((x + 20, y_top + 10), f"{i + 1}. {node_name}", font=font, fill=(0, 0, 0))
        # 점수 출력 (노드 인덱스 범위 내)
        if i < len(score_list):
            d.text((x + 20, y_top + 30), f"점수: {score_list[i]}", font=font, fill=(0, 0, 255))
        # 마지막 노드가 아니면 다음 노드와 연결하는 선 그리기
        if i < len(path_list) - 1:
            d.line(
                [x + node_width, y_top + node_height // 2, x + node_width + node_gap, y_top + node_height // 2],
                fill=(255, 0, 0), width=3
            )
        # 다음 노드 x 위치 이동 (노드 폭 + 간격)
        x += node_width + node_gap

    # 이미지 메모리를 바이트 버퍼에 저장 후 반환
    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

# --- [4단계] 워크플로우 구성 ---
workflow = StateGraph(ChefState)  # 워크플로우 타입으로 선언

# 노드(부서) 등록
workflow.add_node("planner", planner_node)          # 기획부
workflow.add_node("cook", cook_node)                # 제작부
workflow.add_node("marketing", marketing_node)      # 홍보부
workflow.add_node("reviewer", reviewer_node)        # 검수부
############################################################
workflow.add_node("delivery", delivery_node)        # 배달부 (새롭게 추가)
############################################################
workflow.add_node("error_handler", error_handler_node)  # 에러 처리부

workflow.set_entry_point("planner")  # 시작점은 기획부로 설정

# 노드 간 흐름 관계 설정
workflow.add_edge("planner", "cook")        # 기획부 → 제작부
workflow.add_edge("planner", "marketing")   # 기획부 → 홍보부 (병렬)

# 제작부 이후 조건 분기: 에러 발생 시 에러 처리부, 아니면 검수부로 이어짐
workflow.add_conditional_edges("cook", lambda state: "error_handler" if state["errors"] else "reviewer")

workflow.add_edge("marketing", "reviewer")  # 홍보부 → 검수부

# 검수부 → 배달부로 흐름 추가 (새 노드 연결)####
workflow.add_edge("reviewer", "delivery")
###########################################
# 배달부 → 종료
workflow.add_edge("delivery", END)
############################################
# 에러 처리부 → 종료
workflow.add_edge("error_handler", END)

# 워크플로우를 실행 가능한 앱으로 컴파일
app = workflow.compile()

# --- [5단계] Streamlit UI ---
st.title("⚡ 병렬 처리 협업 시스템")

if st.button("시스템 가동"):
    # 빈 상태로 초기 실행
    result = app.invoke({"messages": [], "execution_path": [], "scores": [], "errors": []})

    st.subheader("📝 업무 기록")
    for msg in result["messages"]:
        st.info(msg)  # 각 메시지 정보창으로 출력

    if result["errors"]:
        st.subheader("❌ 에러 로그")
        for err in result["errors"]:
            st.error(err)  # 에러 로그 표시

    st.subheader("🗺️ 병렬 협업 로드맵")
    path_img_data = draw_path_map(result["execution_path"], result["scores"])  # 시각화 이미지 생성
    st.image(path_img_data)  # 이미지 화면 출력

    # 이미지 다운로드 버튼 제공
    st.download_button(
        label="📂 협업 로드맵 저장하기",
        data=path_img_data,
        file_name="collaboration_map.png",
        mime="image/png"
    )