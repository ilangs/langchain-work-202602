# total.py 
# csv 데이터 생성 -> 모델 생성 -> 모델 훈련 -> 학습모델 저장 -> 평가보고서
# train_test_split: 데이터 중 학습용(80%)은 훈련에만 사용, 평가용(20%)는 학습 완료 후 모델이 한 번도 본 적 없는 데이터로 최종 평가

import os, sys, random, itertools, joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split # 핵심 추가

#########################################################################
print("--- [1단계] 스팸 판별 학습용 데이터 생성 ---")
#########################################################################

base_dir = os.path.dirname(os.path.abspath(__file__))

try:
    user_input = input("생성할 데이터 총 개수를 입력하세요 (예: 300, 500, 1000) : ")
    total_count = int(user_input)
    if total_count <= 0:
        raise ValueError
    if total_count % 2 != 0:
        total_count += 1
        print(f"[WARN] 50:50 비율을 위해 개수를 {total_count}개로 조정합니다.")
except ValueError:
    print("[ERROR] 유효한 양의 정수를 입력해주세요.")
    sys.exit(1)

half_n = total_count // 2

# 단어 풀 (10 x 10 x 10 = 최대 1,000 조합 가능)
spam_words1 = ["(광고)", "당첨!", "대출", "주식", "특가", "무료", "VIP", "긴급", "마지막 기회", "초특가"]
spam_words2 = ["최저 금리", "무료 쿠폰", "급등 종목", "최대 80% 할인", "사은품 증정", "수익 보장", "무보증 대출", "포인트 지급", "전액 지원", "특별 이벤트"]
spam_words3 = ["아래 링크를 클릭하세요.", "지금 바로 신청하세요.", "상담 받아보세요.", "다운로드 하세요.", "연락 바랍니다.", "확인해 보세요.", "절대 놓치지 마세요.", "서둘러 참여하세요.", "고객센터로 문의하세요.", "앱에서 확인하세요."]

ham_words1 = ["오늘", "내일", "이번 주", "팀장님", "고객님", "대리님", "프로젝트", "회의", "점심", "다음 주"]
ham_words2 = ["회의 시간", "요청하신 자료", "카드 명세서", "택배 배송", "결제 내역", "업무 보고서", "계약서 초안", "휴가 신청서", "미팅 준비", "일정 변경"]
ham_words3 = ["확인 부탁드립니다.", "송부해 드립니다.", "도착 예정입니다.", "검토 바랍니다.", "언제 시간 되시나요?", "수정 완료했습니다.", "참고 부탁드립니다.", "다시 연락드리겠습니다.", "미리 감사드립니다.", "공지사항 확인 바랍니다."]

spam_comb = list(itertools.product(spam_words1, spam_words2, spam_words3))
ham_comb = list(itertools.product(ham_words1, ham_words2, ham_words3))

if half_n > len(spam_comb):
    print(f"[ERROR] 중복 없이 생성 가능한 최대 개수는 {len(spam_comb)*2}개입니다.")
    sys.exit(1)
    
spam_sentences = [f"{w1} {w2} {w3}" for w1, w2, w3 in spam_comb]
ham_sentences = [f"{w1} {w2} {w3}" for w1, w2, w3 in ham_comb]

content = random.sample(spam_sentences, half_n) + random.sample(ham_sentences, half_n)
labels = [1] * half_n + [0] * half_n  # 1: 스팸, 0: 정상

df = pd.DataFrame({"text": content, "label": labels})
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)
csv_path = os.path.join(data_dir, f"spam_{total_count}.csv")

df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"\n[SUCCESS] 총 {len(df)}개의 데이터가 '{csv_path}'에 저장되었습니다.")
print("\n")

#########################################################################
print("--- [2단계] 학습 모델->생성->훈련->저장 ---")
#########################################################################

# 1. 학습 데이터 준비
df_train = pd.read_csv(csv_path, encoding="utf-8-sig")

# ✨ 핵심 로직: Train / Test Split 적용 (8:2 비율)
X = df_train['text']
y = df_train['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. 사이킷런 파이프라인 설계
model = Pipeline([('tfidf', TfidfVectorizer()),('clf', MultinomialNB())])

# 3. 모델 학습 (전체 데이터가 아닌 80%의 X_train 데이터로만 학습)
print(f"🚀 총 {len(X_train)}개의 데이터로 사이킷런 모델 학습 시작...")
model.fit(X_train, y_train)  
print("✅ 학습 완료!\n")

# 4. 샘플 3개 문장 추론 테스트 (가상 테스트)
test_texts = [
    "안녕하세요 팀장님, 내일 점심 식사 가능하신가요?",
    "축하합니다! 1억 원 경품에 당첨되셨습니다. 지금 클릭!",
    "광고) 최저 금리 대출 상품 안내 드립니다."
]

predictions = model.predict(test_texts)
probabilities = model.predict_proba(test_texts)

# 5. 학습 결과 저장
model_filename = os.path.join(data_dir, f'finance_spam_model_{total_count}.pkl')
joblib.dump(model, model_filename)

# 6. 결과 출력
print("\n🔍 3개 샘플 문장 분석 결과 (Sanity Check):")
for text, pred, prob in zip(test_texts, predictions, probabilities):
    label = "🚨 스팸(SPAM)" if pred == 1 else "⭐ 정상(HAM)"
    score = round(prob[pred] * 100, 2)
    print(f"메일 내용: {text}")
    print(f"분석 결과: {label} (확신도: {score}%)")
    print("-" * 50)
print("\n")

#########################################################################
print("--- [3단계] 평가 보고서 산출 ---")
#########################################################################
print(f"📊 모델이 한 번도 본 적 없는 {len(X_test)}개의 Test 데이터로 신뢰도 검증을 수행합니다.")

# 1. 분리해둔 20%의 테스트 데이터(X_test)로 실제 예측값 생성
y_pred = model.predict(X_test)       

# 2. 정확도(Accuracy) 계산: 
# y_true는 위에서 분리한 정답 레이블인 y_test가 됩니다.
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ 테스트 세트 모델 정확도: {accuracy * 100:.2f}%\n")

# 3. 상세 보고서(F1-score, Precision, Recall, support) 산출
report = classification_report(y_test, y_pred, target_names=['정상(HAM)', '스팸(SPAM)'])
print("--- 상세 평가 보고서 ---")
print(report)

# 4. 혼동 행렬(Confusion Matrix)
conf_matrix = confusion_matrix(y_test, y_pred)
df_conf = pd.DataFrame(conf_matrix, columns=['예측_정상', '예측_스팸'], index=['실제_정상', '실제_스팸'])
print("--- 혼동 행렬 (Confusion Matrix) ---")
print(df_conf)
