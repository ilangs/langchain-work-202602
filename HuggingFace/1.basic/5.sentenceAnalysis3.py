import streamlit as st  # Streamlit 웹 프레임워크 라이브러리 임포트
from transformers import pipeline  # Hugging Face의 사전 학습된 모델 파이프라인 임포트
import matplotlib.pyplot as plt  # 데이터 시각화를 위한 Matplotlib 라이브러리 임포트
import pandas as pd  # 데이터프레임 생성 및 표 출력을 위한 Pandas 임포트
from collections import Counter  # 리스트 내 요소별 개수를 세기 위한 도구 임포트
import platform  # 현재 실행 중인 운영체제(Windows, Mac 등)를 확인하기 위해 임포트

# 0. 한글 폰트 설정 함수 (그래프 깨짐 방지)
def set_korean_font():
    # 그래프에서 마이너스(-) 기호가 깨지는 현상을 방지하기 위한 설정
    plt.rcParams['axes.unicode_minus'] = False 
    
    # 현재 시스템의 운영체제를 확인하여 적절한 한글 폰트 적용
    os_name = platform.system()
    if os_name == 'Windows':
        # 윈도우 환경: '맑은 고딕' 설정
        plt.rc('font', family='Malgun Gothic')
    elif os_name == 'Darwin':
        # macOS 환경: 'AppleGothic' 설정
        plt.rc('font', family='AppleGothic')
    else:
        # 리눅스나 기타 환경: '나눔고딕' 설정 (설치되어 있다고 가정)
        plt.rc('font', family='NanumGothic')

# 정의한 폰트 설정 함수를 실행하여 Matplotlib에 적용
set_korean_font()

# 1. 모델 로드 (캐싱 기능 사용: 앱 실행 시 한 번만 로드하여 메모리 효율 증대)
@st.cache_resource
def load_model():
    # nlptown의 다국어 지원 BERT 모델 로드 (1~5 별점 형태의 감정 분석)
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# 모델 객체 생성
classifier = load_model()

# 2. 웹 페이지 레이아웃 및 제목 설정
st.set_page_config(page_title="Sentiment Dashboard", layout="wide") # 전체 화면 모드 설정
st.title("📊 감정 분석 및 데이터 시각화 (한글 최적화)") # 메인 타이틀
st.markdown("### 30년 차 팀장의 실무 가이드: 시각화 전문 코드") # 서브 타이틀

# 분석할 샘플 문장 정의 (사용자가 요청한 세 문장)
default_text = """오늘은 날씨가 좋아서 기분이 상쾌합니다.
경제 뉴스가 불안해서 마음이 무겁습니다.
새로운 영화가 정말 재미있었습니다."""

# 사용자로부터 텍스트를 입력받는 멀티라인 입력창 (높이 150픽셀)
user_input = st.text_area("분석할 문장들을 입력하세요 (줄바꿈으로 구분):", default_text, height=150)

# '분석 실행' 버튼 클릭 시 로직 가동
if st.button("데이터 분석 및 그래프 생성"):
    # 입력된 텍스트를 줄바꿈('\n') 기준으로 나누고, 앞뒤 공백 제거 및 빈 줄 필터링
    sentences = [s.strip() for s in user_input.split('\n') if s.strip()]
    
    # 분석할 문장이 하나도 없을 경우 경고 메시지 출력
    if not sentences:
        st.warning("분석할 문장을 최소 한 개 이상 입력해주세요.")
    else:
        results_list = [] # 테이블 출력용 데이터를 담을 리스트
        star_counts = []  # 그래프 집계용 별점 숫자를 담을 리스트

        # 3. 인공지능 모델을 이용한 감정 분석 수행 루프
        for text in sentences:
            res = classifier(text)[0] # 모델 실행 결과의 첫 번째 요소 추출
            star_label = res['label'] # 결과 레이블 (예: '1 star', '5 stars')
            star_num = int(star_label.split()[0]) # '1 star' 문자열에서 숫자 '1'만 추출하여 정수 변환
            
            # 분석 결과를 딕셔너리 형태로 리스트에 추가
            results_list.append({
                "입력 문장": text,
                "감정 결과(별점)": star_label,
                "예측 확률": f"{res['score']:.2%}" # 신뢰도를 백분율로 표기
            })
            star_counts.append(star_num) # 통계를 위해 별점 숫자 저장

        # 4. 분석 결과 테이블(표) 출력
        st.subheader("📋 분석 상세 데이터")
        st.table(pd.DataFrame(results_list)) # Pandas를 이용해 깔끔한 표 형식으로 렌더링

        # 5. 시각화 그래프 작성 (Matplotlib)
        st.subheader("📈 감정 분포 현황 (시각화)")
        
        # 1점부터 5점까지 각 점수가 몇 번 나왔는지 카운트
        counts = Counter(star_counts)
        x_stars = [f"{i} Stars" for i in range(1, 6)] # X축 눈금 이름 생성
        y_counts = [counts.get(i, 0) for i in range(1, 6)] # Y축에 들어갈 실제 빈도수 추출

        # 그래프 크기 설정 (가로 8인치, 세로 4인치)
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # 막대 그래프 생성 (파스텔 톤 색상 조합 적용)
        colors = ['#ff9999', '#ffcc99', '#ffff99', '#b3ffb3', '#66b3ff']
        bars = ax.bar(x_stars, y_counts, color=colors, edgecolor='gray', linewidth=0.8)
        
        # 그래프 텍스트 설정 (한글 폰트 적용 확인)
        ax.set_xlabel("감정 등급 (별점)", fontsize=11)
        ax.set_ylabel("문장 개수 (건)", fontsize=11)
        ax.set_title("입력 데이터의 감정 분포 결과", fontsize=14, fontweight='bold')
        
        # Y축 눈금을 데이터 최대치에 맞춰 정수 단위로 조정
        ax.set_yticks(range(0, max(y_counts) + 2))
        
        # 막대 상단에 해당 문장 개수를 텍스트로 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{int(height)}건', ha='center', va='bottom', fontsize=10)

        # 6. 완성된 그래프를 Streamlit 화면에 표시
        st.pyplot(fig)