# 4.nlptownAnalysis1.py파일 작성
# pipeline => 데이터 수집->모델훈련->성능테스트->결과까지 한꺼번에 처리
from transformers import pipeline

# --- [1. 감정 분석 파이프라인 생성] ---
# 'nlptown/bert-base-multilingual-uncased-sentiment' 모델은
# 한국어 포함 여러 언어의 문장을 1~5점으로 감정 분류합니다.
classifier = pipeline(
    "sentiment-analysis",  # 태스크 종류: 감정 분석
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)
# --- [2. 분석할 한국어 문장 입력] ---
# 예시 문장: 긍정적인 뉴스 기사
news_text = "오늘은 날씨가 맑고 따뜻해서 산책하기에 정말 좋은 하루입니다."

# --- [3. 감정 분석 실행] ---
# pipeline 객체에 문장을 넣으면 결과가 리스트 형태로 반환됩니다.
result = classifier(news_text)
# --- [4. 결과 출력] --- #이 모델은 긍정/부정뿐 아니라 세밀한 감정 강도(1~5점)까지 알려주기 때문에,
#                        뉴스 기사나 리뷰 텍스트의 감정을 더 정밀하게 분석할 수 있다.
# 결과는 [{'label': '5 stars', 'score': 0.95}] 형태로 반환됩니다.
# label: 1~5 stars (별점), score: 확률 점수
print("뉴스 기사:", news_text)
print("감정 분석 결과:", result[0]['label'])  # 감정 라벨 출력 (예: '5 stars')
print("확률 점수:", round(result[0]['score'], 4))  # 신뢰도 점수 출력

# 감정을 평가 1,2점->부정, 3점->중립, 4,5점->긍정
'''
뉴스 기사: 오늘은 날씨가 맑고 따뜻해서 산책하기에 정말 좋은 하루입니다.
감정 분석 결과: 5 stars
확률 점수: 0.4461
'''
