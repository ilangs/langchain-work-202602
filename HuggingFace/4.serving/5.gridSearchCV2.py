# 5.gridSearchCV.py -> 5.gridSearchCV2.py copy-paste 후 수정 w/ LLM
# param_grid값을 임의로 조절 입력하여 어느 시점에 가장 오차가 적은지를 확인(평균MAE)하여 그래프로 출력

import FinanceDataReader as fdr
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV

# 한글 폰트 설정 (Windows 기준, Mac은 'AppleGothic')
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 테스트용 데이터 로드 (삼성전자 예시)
ticker = "005930"
start_date = "2022-01-01" # 충분한 학습 데이터 확보를 위해 기간 조정
end_date = datetime.datetime.today().strftime("%Y-%m-%d")

print(f"📅 데이터 로딩 중... ({ticker})")
df = fdr.DataReader(ticker, start_date, end_date)
df.reset_index(inplace=True)

# 2. 특성 공학 (Feature Engineering)
df['day'] = df['Date'].dt.day
df['month'] = df['Date'].dt.month
df['year'] = df['Date'].dt.year
df['weekday'] = df['Date'].dt.weekday
df['lag1'] = df['Close'].shift(1)
df['lag2'] = df['Close'].shift(2)
df['lag3'] = df['Close'].shift(3)

df.dropna(inplace=True)

features = ['day', 'month', 'year', 'weekday', 'lag1', 'lag2', 'lag3']
X = df[features]
y = df['Close']

# 3. GridSearchCV 설정 (파라미터 조합 확장)
# 총 조합 수: 3 * 3 * 3 * 2 = 54가지
param_grid = {
    'n_estimators': [100, 300, 500],      # 나무의 개수
    'learning_rate': [0.01, 0.05, 0.1],   # 학습 속도
    'max_depth': [3, 5, 7],               # 나무의 깊이
    'subsample': [0.8, 1.0]               # 데이터 샘플링 비율
}

base_model = XGBRegressor(n_jobs=-1, random_state=42)

grid_search = GridSearchCV(
    estimator=base_model,
    param_grid=param_grid,
    cv=3,                                # 3-Fold 교차 검증
    scoring='neg_mean_absolute_error',   # 평가 지표: 음수 MAE
    verbose=1
)

# 4. 최적화 실행
print("\n🚀 최적의 파라미터 탐색 시작 (전체 조합: 54개)...")
grid_search.fit(X, y)

# 5. 결과 분석 및 데이터 가공
# GridSearchCV의 모든 실험 결과를 DataFrame으로 변환
results_df = pd.DataFrame(grid_search.cv_results_)

# neg_mean_absolute_error를 양수인 MAE로 변환 (작을수록 좋음)
results_df['MAE'] = -results_df['mean_test_score']

# 그래프 표시를 위해 파라미터 조합을 문자열로 요약
def make_param_label(p):
    return f"LR:{p['learning_rate']}, Depth:{p['max_depth']}, Est:{p['n_estimators']}, Sub:{p['subsample']}"

results_df['params_label'] = results_df['params'].apply(make_param_label)

# MAE 기준 오름차순 정렬 (오차가 적은 순서)
results_df = results_df.sort_values(by='MAE').reset_index(drop=True)

# 6. 결과 시각화
plt.figure(figsize=(12, 10))
# 성능이 좋은 상위 15개 조합 출력
top_n = 15
plot_data = results_df.head(top_n)

# 가로 바 차트 생성
bars = plt.barh(plot_data['params_label'], plot_data['MAE'], color='skyblue')
plt.xlabel('평균 오차 (MAE)', fontsize=12)
plt.ylabel('파라미터 조합 (Learning Rate, Depth, Estimators, Subsample)', fontsize=12)
plt.title(f'XGBoost 하이퍼파라미터 조합별 MAE 비교 (상위 {top_n}개)', fontsize=15)
plt.gca().invert_yaxis() # 오차가 가장 적은 것이 위로 오게 뒤집기

# 바 끝에 MAE 값 텍스트 표시
for bar in bars:
    width = bar.get_width()
    plt.text(width + 10, bar.get_y() + bar.get_height()/2, f'{width:.2f}원', 
             va='center', ha='left', fontsize=9, fontweight='bold')

plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 7. 최종 결과 리포트
print("\n" + "="*60)
print("📊 [GridSearchCV 최종 결과 리포트]")
print(f"최적의 설정값: {grid_search.best_params_}")
print(f"최고의 평균 오차(MAE): {results_df.loc[0, 'MAE']:.2f}원")
print("="*60)

# 최적 모델로 마지막 데이터 예측 테스트
best_model = grid_search.best_estimator_
last_prediction = best_model.predict(X.tail(1))
actual_last_close = y.iloc[-1]

print(f"실제 마지막 종가: {int(actual_last_close):,}원")
print(f"최적 모델 예측값: {int(last_prediction[0]):,}원")

'''
📅 데이터 로딩 중... (005930)

🚀 최적의 파라미터 탐색 시작 (전체 조합: 54개)...
Fitting 3 folds for each of 54 candidates, totalling 162 fits

-> 그래프 생성: 5.result_gridSearchCV2.png

============================================================
📊 [GridSearchCV 최종 결과 리포트]
최적의 설정값: {'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 100, 'subsample': 1.0}
최고의 평균 오차(MAE): 6675.37원
============================================================
실제 마지막 종가: 173,500원
최적 모델 예측값: 178,110원
'''

