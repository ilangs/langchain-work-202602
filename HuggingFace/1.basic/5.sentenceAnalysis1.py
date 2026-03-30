import streamlit as st
from transformers import pipeline

# 1. 모델 로드 (Hugging Face의 nlptown BERT 모델 사용)
# 'sentiment-analysis' 파이프라인은 텍스트 분류를 위한 가장 간편한 방법입니다.
@st.cache_resource # 메모리 효율성
def load_model():
    # 모델 경로: nlptown/bert-base-multilingual-uncased-sentiment
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

classifier = load_model() # 함수의 반환값을 이용해서 작성

# 2. UI 구성
st.title("📊 다국어 문장 감정 분석기")
st.subheader("30년 차 팀장의 실무 예제: BERT 모델 활용")

# 입력 데이터 정의 (사용자가 요청한 세 문장)
default_sentences = [
    "오늘은 날씨가 좋아서 기분이 상쾌합니다.",
    "경제 뉴스가 불안해서 마음이 무겁습니다.",
    "새로운 영화가 정말 재미있었습니다."
]

# 텍스트 영역에 기본값으로 설정
user_input = st.text_area("분석할 문장들을 입력하세요 (줄바꿈으로 구분):", "\n".join(default_sentences))

if st.button("분석 시작"):
    sentences = user_input.split('\n') # 줄바꿈을 기준으로 문장 분리
    
    st.write("---")
    
    # 3. 결과 출력 루프
    for i, text in enumerate(sentences):
        if text.strip(): # 빈 줄이 아닐 경우에만 실행
            # 모델을 통해 감정 분석 수행
            result = classifier(text)[0] 
            
            label = result['label']      # 결과 레이블 (예: 1 star, 5 stars)
            score = result['score']      # 예측 확률 (신뢰도)
            
            # 보기 좋게 결과 표시
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info(f"**문장 {i+1}:** {text}")
            with col2:
                # 점수(stars)에 따라 긍정/부정 판단 (실무적 해석)
                sentiment_val = int(label.split()[0])
                color = "green" if sentiment_val >= 4 else "red" if sentiment_val <= 2 else "orange"
                st.markdown(f":{color}[**결과: {label}**]")
                st.caption(f"확률: {score:.2%}")