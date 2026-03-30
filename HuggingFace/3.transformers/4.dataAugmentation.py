# 4.dataAugmentation.py (데이터를 증강시켜서 성능을 향상시킨다.)

from sklearn.feature_extraction.text import TfidfVectorizer  # 텍스트를 숫자로 변환하는 도구
from sklearn.naive_bayes import MultinomialNB                # 스팸 분류에 특화된 AI 모델 (확률계산)
from sklearn.pipeline import Pipeline                        # 전과정을 하나로 묶어주는 파이프라인
import joblib    # 왼성된 AI 모델을 vkdlf(.pkl)로 저장하거나 다시 읽어올때 사용
# 추가
import os
import pandas as pd

# 1. 학습 데이터 준비 - 500개 학습 데이터 준비 spam_500.csv
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "data", "spam_500.csv")
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 2. 사이킷런 파이프라인 설계
# 텍스트 변환(TF-IDF)과 모델(Naive Bayes)을 하나의 공정으로 묶습니다.
model = Pipeline([
    ('tfidf', TfidfVectorizer()),   # 단어의 중요도를 계산해 숫자로 바꿈
    ('clf', MultinomialNB())        # 나이브 베이즈 알고리즘으로 분류
])

# 3. 모델 학습 (딥러닝보다 훨씬 빠릅니다!)
print("🚀 사이킷런 모델 학습 시작...")
model.fit(df['text'], df['label'])  
print("✅ 학습 완료!")

# 4. 새로운 데이터로 테스트 (추론)
test_texts = [
    "안녕하세요 팀장님, 내일 점심 식사 가능하신가요?",
    "축하합니다. 무료상품권에 당첨되었습니다.",
    "축하합니다! 1억 원 경품에 당첨되셨습니다. 지금 클릭!",
    "광고) 최저 금리 대출 상품 안내 드립니다."
]

predictions = model.predict(test_texts)         # 스팸 여부 (0 또는 1)
probabilities = model.predict_proba(test_texts) # 확신도(확률로 계산)

# 5. 학습 결과 저장
model_filename = os.path.join(base_dir, 'data', 'finance_spam_model_500.pkl')
joblib.dump(model, model_filename)

# 6. 결과 출력
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
분석 결과: ★ 정상(HAM) (확신도: 98.65%)
--------------------------------------------------
메일 내용: 축하합니다! 1억 원 경품에 당첨되셨습니다. 지금 클릭!
분석 결과: 🚨 스팸(SPAM) (확신도: 92.49%)
--------------------------------------------------
메일 내용: 광고) 최저 금리 대출 상품 안내 드립니다.
분석 결과: 🚨 스팸(SPAM) (확신도: 96.58%)
--------------------------------------------------
'''