# --- [필수 라이브러리 임포트] ---
import streamlit as st  # 웹 UI를 만들기 위한 Streamlit 라이브러리 불러오기
from transformers import pipeline  # Hugging Face의 모델 실행 도구(pipeline) 불러오기
import matplotlib.pyplot as plt  # 그래프(시각화)를 그리기 위한 matplotlib 불러오기

# --- [1. 감정 분석 파이프라인 생성] ---
classifier = pipeline(
    "sentiment-analysis",  # 수행할 작업: 감정 분석
    model="nlptown/bert-base-multilingual-uncased-sentiment",  # 다국어 감정 분석 모델
    framework="pt"  # PyTorch 기반으로 실행
)

# --- [2. 한글 폰트 간단 설정] ---
plt.rc("font", family="Malgun Gothic")  # matplotlib에서 사용할 기본 폰트를 나눔고딕으로 설정
plt.rcParams["axes.unicode_minus"] = False  # 그래프에서 마이너스(-) 기호 깨짐 방지

# --- [3. Streamlit 페이지 설정] ---
st.set_page_config(page_title="한국어 평균 감정 분석기", layout="wide")  # 웹 페이지 제목과 레이아웃 설정
st.title("🌟 여러 문장 평균 감정 분석기 (별점 시각화)")  # 화면에 표시할 메인 제목

# --- [4. 사용자 입력 받기] ---
user_texts = st.text_area(
    "분석할 문장을 여러 개 입력하세요 (줄바꿈으로 구분):",  # 입력창 설명
    "오늘은 날씨가 좋아서 기분이 상쾌합니다.\n경제 뉴스가 불안해서 마음이 무겁습니다.\n새로운 영화가 정말 재미있었습니다."  # 기본 입력값
)

# --- [5. 감정 분석 실행] ---
if user_texts.strip():  # 입력값이 공백이 아닌 경우에만 실행
    sentences = user_texts.split("\n")  # 줄바꿈 기준으로 문장들을 리스트로 분리
    results = []  # 별점 점수를 저장할 빈 리스트 생성

    for sent in sentences:  # 각 문장을 하나씩 반복 처리
        if sent.strip():  # 공백 문장은 제외
            res = classifier(sent.strip())[0]  # 감정 분석 수행 후 첫 번째 결과 추출
            stars = int(res['label'].split()[0])  # '5 stars'에서 숫자(5)만 추출하여 정수로 변환
            results.append(stars)  # 별점 리스트에 추가

            # --- [결과 출력] ---
            st.write(f"문장: {sent}")  # 입력 문장 출력
            st.write(f"감정 분석 결과: {res['label']} (확률: {round(res['score'],4)})")  # 분석 결과 출력
            st.divider()  # 문장 간 구분선 추가

    # --- [6. 평균 별점 계산] ---
    if results:  # 분석된 결과가 하나라도 있을 경우
        avg_score = sum(results) / len(results)  # 평균 별점 계산
        st.subheader(f"📊 전체 평균 별점: {avg_score:.2f} / 5")  # 평균 결과 출력

        # --- [7. 시각화 (히스토그램)] ---
        fig, ax = plt.subplots()  # 그래프를 그릴 figure와 axis 생성
        ax.hist(
            results,  # 별점 데이터
            bins=[0.5,1.5,2.5,3.5,4.5,5.5],  # 별점 구간 설정
            rwidth=0.8,  # 막대 너비 설정
            color="skyblue",  # 막대 색상
            edgecolor="black"  # 테두리 색상
        )
        ax.set_xticks([1,2,3,4,5])  # X축 눈금을 1~5로 설정
        ax.set_xticklabels(["⭐1","⭐2","⭐3","⭐4","⭐5"])  # X축 레이블에 별 표시 추가
        ax.set_xlabel("별점")  # X축 이름 설정
        ax.set_ylabel("문장 개수")  # Y축 이름 설정
        ax.set_title("문장별 감정 분석 분포")  # 그래프 제목 설정

        st.pyplot(fig)  # Streamlit 화면에 그래프 출력