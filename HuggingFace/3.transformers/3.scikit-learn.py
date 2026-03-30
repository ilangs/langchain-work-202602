# 3.scikit-learn.py파일 작성

from sklearn.feature_extraction.text import TfidfVectorizer  # 텍스트를 숫자로 변환하는 도구
from sklearn.naive_bayes import MultinomialNB                # 스팸 분류에 특화된 AI 모델 (확률계산)
from sklearn.pipeline import Pipeline                        # 전과정을 하나로 묶어주는 파이프라인
# 추가
import joblib    # 왼성된 AI 모델을 vkdlf(.pkl)로 저장하거나 다시 읽어올때 사용
# 추가
import os

# 1. 학습 데이터 준비
train_texts = [
    "당첨! 무료 쿠폰을 받으려면 아래 링크를 클릭하세요.",
    "오늘 회의 시간은 오후 3시입니다. 확인 부탁드려요.",
    "입금 확인 바랍니다. 이번 달 카드 명세서입니다.",
    "대출 최저 금리 보장! 지금 바로 상담 신청하세요.",
    "팀장님, 요청하신 보고서 초안 송부드립니다."
]
train_labels = [1, 0, 0, 1, 0]  # 1: 스팸, 0: 정상

# 2. 사이킷런 파이프라인 설계
# 텍스트 변환(TF-IDF)과 모델(Naive Bayes)을 하나의 공정으로 묶습니다.
model = Pipeline([
    ('tfidf', TfidfVectorizer()),   # 단어의 중요도를 계산해 숫자로 바꿈
    ('clf', MultinomialNB())        # 나이브 베이즈 알고리즘으로 분류
])

# 3. 모델 학습 (딥러닝보다 훨씬 빠릅니다!)
print("🚀 사이킷런 모델 학습 시작...")
model.fit(train_texts, train_labels)
print("✅ 학습 완료!")

# 4. 새로운 데이터로 테스트 (추론)
test_texts = [
    "안녕하세요 팀장님, 내일 점심 식사 가능하신가요?",
    "축하합니다! 1억 원 경품에 당첨되셨습니다. 지금 클릭!",
    "광고) 최저 금리 대출 상품 안내 드립니다."
]

predictions = model.predict(test_texts)         # 스팸 여부 (0 또는 1)
probabilities = model.predict_proba(test_texts) # 확신도(확률로 계산)

# [추가] 학습 결과 저장
base_dir = os.path.dirname(os.path.abspath(__file__))
model_filename = os.path.join(base_dir, 'data', 'finance_spam_model.pkl')
joblib.dump(model, model_filename)

# 5. 결과 출력
print("\n🔍 분석 결과:")
for text, pred, prob in zip(test_texts, predictions, probabilities):
    label = "🚨 스팸(SPAM)" if pred == 1 else "★ 정상(HAM)"
    # 해당 클래스로 예측한 확률값 추출
    score = round(prob[pred] * 100, 2)
    
    print(f"메일 내용: {text}")
    print(f"분석 결과: {label} (확신도: {score}%)")
    print("-" * 50)


'''
🚀 사이킷런 모델 학습 시작...
✅ 학습 완료!

🔍 분석 결과:
메일 내용: 안녕하세요 팀장님, 내일 점심 식사 가능하신가요?
분석 결과: ★ 정상(HAM) (확신도: 67.42%)
--------------------------------------------------
메일 내용: 축하합니다! 1억 원 경품에 당첨되셨습니다. 지금 클릭!
분석 결과: ★ 정상(HAM) (확신도: 51.37%)
--------------------------------------------------
메일 내용: 광고) 최저 금리 대출 상품 안내 드립니다.
분석 결과: 🚨 스팸(SPAM) (확신도: 55.03%)
--------------------------------------------------
'''
