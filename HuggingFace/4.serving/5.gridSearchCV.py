import FinanceDataReader as fdr
import pandas as pd
import datetime
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV

# 1. 테스트용 데이터 로드 (삼성전자 예시)
ticker = "005930"
start_date = "2020-01-01"
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

# 과거 데이터가 없는 초기 행(NaN)들은 제거
df.dropna(inplace=True)

# 학습 데이터 분리
features = ['day', 'month', 'year', 'weekday', 'lag1', 'lag2', 'lag3']
X = df[features]
y = df['Close']

# 3. GridSearchCV 설정
# 테스트하고 싶은 파라미터 후보군 (조합: 2x2x2x2 = 16가지)
param_grid = {
    'n_estimators': [100, 200],         # 나무의 개수
    'learning_rate': [0.05, 0.1],       # 학습 속도
    'max_depth': [3, 5],                # 나무의 깊이
    'subsample': [0.8, 1.0]             # 데이터 샘플링 비율
}

# 기본 모델 설정 (n_jobs=-1은 내 컴퓨터의 모든 CPU 사용)
base_model = XGBRegressor(n_jobs=-1, random_state=42)

# GridSearch 객체 생성 (cv=3은 3번의 교차 검증 실시)
grid_search = GridSearchCV(
    estimator=base_model,               # 테스트할 모델
    param_grid=param_grid,              # 훈련시킬 설정값 부여
    cv=3,                               # 교차검증 하겠다는 표시
    scoring='neg_mean_absolute_error',  # 오차가 가장 적은 모델 찾기
    verbose=2                           # 실행 과정을 상세히 출력
)

# 4. 최적화 실행 (가장 중요한 부분)
print("\n🚀 최적의 파라미터 탐색 시작...")
grid_search.fit(X, y)

# 5. 결과 리포트
print("\n" + "="*50)
print("📊 [GridSearchCV 결과 리포트]")
print(f"최적의 설정값: {grid_search.best_params_}")
print(f"최고의 평균 오차(MAE): {-grid_search.best_score_:.2f}원")
print("="*50)

# 최적의 모델로 마지막 데이터 예측 테스트
best_model = grid_search.best_estimator_
last_prediction = best_model.predict(X.tail(1))
actual_last_close = y.iloc[-1]

print(f"실제 마지막 종가: {int(actual_last_close):,}원")
print(f"최적 모델 예측값: {int(last_prediction[0]):,}원")

'''
==================================================
📊 [GridSearchCV 결과 리포트]
최적의 설정값: {'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 100, 'subsample': 0.8}
최고의 평균 오차(MAE): 4760.86원
==================================================
실제 마지막 종가: 172,800원
최적 모델 예측값: 177,063원
'''
