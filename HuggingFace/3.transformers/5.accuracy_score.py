# 5.accuracy_score.py 파일 작성

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd

# 1. 실제 정답(Y_true)과 모델이 예측한 값(Y_pred)을 준비합니다.
# (실무에서는 model.predict()의 결과값을 넣게 됩니다)
y_true = [1, 0, 0, 1, 0, 1, 0, 0, 1, 1]  # 실제 정답 (1: 스팸, 0: 정상)
y_pred = [1, 0, 0, 0, 0, 1, 1, 0, 1, 1]  # AI가 예측한 값

# 2. 정확도(Accuracy) 계산: 전체 중 몇 개나 맞췄는가?
accuracy = accuracy_score(y_true, y_pred)
print(f"✅ 모델 정확도: {accuracy * 100}%")

# 3. 상세 보고서(F1-score, Precision, Recall, support) 출력
# Precision(정밀도): 스팸이라고 한 것 중 진짜 스팸인 비율
# Recall(재현율): 실제 스팸 중 스팸이라고 맞춘 비율
# F1-score: 위 두 값의 조화평균 (불균형 데이터에서 가장 중요!)
# support: 갯수
report = classification_report(y_true, y_pred, target_names=['정상(HAM)', '스팸(SPAM)'])
print("\n--- 상세 평가 보고서 ---")
print(report)

# 4. 혼동 행렬(Confusion Matrix) 만들기
# 어디서 헷갈렸는지 표로 확인합니다.
conf_matrix = confusion_matrix(y_true, y_pred)
df_conf = pd.DataFrame(conf_matrix,columns=['예측_정상', '예측_스팸'],index=['실제_정상', '실제_스팸'])
print("\n--- 혼동 행렬 (Confusion Matrix) ---")
print(df_conf)

'''
✅ 모델 정확도: 80.0%

--- 상세 평가 보고서 ---
              precision    recall  f1-score   support

     정상(HAM)       0.80      0.80      0.80         5
    스팸(SPAM)       0.80      0.80      0.80         5

    accuracy                           0.80        10
   macro avg       0.80      0.80      0.80        10
weighted avg       0.80      0.80      0.80        10


--- 혼동 행렬 (Confusion Matrix) ---
       예측_정상  예측_스팸
실제_정상      4      1
실제_스팸      1      4
'''