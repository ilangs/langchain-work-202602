# 5.sentenceAnalysis.py 작성
# "오늘은 날씨가 좋아서 기분이 상쾌합니다.\n
# 경제 뉴스가 불안해서 마음이 무겁습니다.\n
# 새로운 영화가 정말 재미있었습니다."의 세문장을 streamlit 화면에서 입력을 받아서 
# nlptown/bert-base-multilingual-uncased-sentiment 모델을 이용해서 
# 문장과 감정분석결과,확률을 화면 출력하는 프로그램을 작성하시오.
# x축은 별점, y축은 문장개수로 표시되는 matplotlib 그래프를 포함하세요.
# 막대 색상은 1~5 별점별로 그라데이션 표현하고, 코드 각 라인마다 주석을 달아 주세요.

import streamlit as st  # Streamlit 웹 프레임워크 임포트
from transformers import pipeline  # Hugging Face의 NLP 파이프라인 임포트
import matplotlib.pyplot as plt  # 데이터 시각화를 위한 matplotlib 임포트
import platform  # 운영체제 확인을 위한 모듈 임포트
from collections import Counter  # 리스트 요소의 개수를 세기 위한 모듈 임포트
import matplotlib.cm as cm  # 컬러맵(색상 그라데이션) 사용을 위한 임포트

# --- [0. matplotlib 한글 깨짐 방지 설정 함수] ---
def set_korean_font():
    """운영체제별로 적합한 한글 폰트를 설정하는 함수"""
    if platform.system() == 'Darwin':  # 맥 OS인 경우
        plt.rc('font', family='AppleGothic')
    elif platform.system() == 'Windows':  # 윈도우 OS인 경우
        plt.rc('font', family='Malgun Gothic')
    plt.rc('axes', unicode_minus=False)  # 마이너스 기호 깨짐 방지

# 앱 제목 설정
st.title("한국어 문장 감정 분석 (BERT)")

# --- [1. 감정 분석 모델 로드 (캐싱 적용)] ---
@st.cache_resource  # 모델을 한 번만 로드하여 성능 최적화
def load_model():
    # 다국어 감정 분석에 특화된 BERT 모델 경로 지정 (1~5 stars 출력)
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    return pipeline("sentiment-analysis", model=model_name)

# 파이프라인 객체 생성
classifier = load_model()

# --- [2. 사용자 입력 섹션] ---
# 기본 예제 문장 설정
default_text = (
    "오늘은 날씨가 좋아서 기분이 상쾌합니다.\n"
    "경제 뉴스가 불안해서 마음이 무겁습니다.\n"
    "새로운 영화가 정말 재미있었습니다."
)

# 텍스트 입력 영역 생성
input_text = st.text_area("분석할 문장을 입력하세요 (줄바꿈으로 구분)", value=default_text, height=150)

# 분석 실행 버튼 클릭 시 로직 시작
if st.button("감정 분석 실행"):
    if input_text.strip():  # 입력값이 비어있지 않은 경우
        # 줄바꿈 기준으로 문장을 분리하고 양끝 공백 제거
        sentences = [s.strip() for s in input_text.strip().split("\n") if s.strip()]
        
        # BERT 모델로 문장 분석 수행 (결과는 리스트 형태)
        results = classifier(sentences)

        st.subheader("📊 감정 분석 상세 결과")
        
        star_labels = []  # 별점 라벨 저장용 리스트
        
        # 분석 결과 화면 출력 및 데이터 수집
        for idx, (sentence, result) in enumerate(zip(sentences, results), 1):
            label = result['label']  # '1 star' ~ '5 stars'
            score = round(result['score'], 4)  # 확신도(확률) 소수점 4자리 반올림
            star_labels.append(label)  # 통계용 리스트에 추가
            
            # 각 문장별 결과를 컨테이너에 표시
            with st.container():
                st.info(f"[{idx}] 문장: **{sentence}** ▷ 판정: **{label}** ▷ 신뢰도: **{score}**")

        # --- [3. 별점별 빈도수 그라데이션 그래프 출력] ---
        st.subheader("📈 별점 분포 통계")
        
        set_korean_font()  # 그래프 한글 설정 적용
        
        # X축에 표시될 고정 카테고리 정의
        categories = ['1 star', '2 stars', '3 stars', '4 stars', '5 stars']
        # 각 별점별 문장 개수 집계
        counts = Counter(star_labels)
        y_values = [counts[cat] for cat in categories]
        
        # 1~5점 순서대로 진해지는 컬러맵 설정 (Red-Yellow-Green 계열의 RdYlGn 사용 가능)
        # 여기서는 부드러운 파란색 계열 그라데이션('Blues') 사용
        colors = cm.get_cmap('Blues')([0.3, 0.45, 0.6, 0.75, 0.9])
        
        # 그래프 객체(Figure) 및 축(Axis) 생성
        fig, ax = plt.subplots()
        # 막대 그래프 생성 (색상 리스트 적용)
        bars = ax.bar(categories, y_values, color=colors, edgecolor='gray')
        
        # Y축 범위를 정수 단위로 깔끔하게 설정
        max_count = max(y_values) if y_values else 1
        ax.set_ylim(0, max_count + 1)
        ax.set_yticks(range(0, int(max_count) + 2))
        
        # 그래프 레이블 및 제목 설정
        ax.set_xlabel("감정 별점 레벨")
        ax.set_ylabel("문장 개수 (건)")
        ax.set_title("분석 문장의 별점별 분포")
        
        # 각 막대 상단에 실제 개수 숫자 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')

        # Streamlit 화면에 그래프 렌더링
        st.pyplot(fig)
    else:
        # 텍스트 미입력 시 경고 메시지
        st.warning("분석할 문장을 입력해 주세요.")