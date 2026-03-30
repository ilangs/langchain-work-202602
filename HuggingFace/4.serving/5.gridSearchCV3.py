# 5.gridSearchCV3.py -> 강사 작성

import FinanceDataReader as fdr
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
import matplotlib.pyplot as plt

# 1. 데이터 로드 및 간단한 전처리
ticker = "000660" # SK하이닉스
df = fdr.DataReader(ticker, "2020-01-01")
df['lag1'] = df['Close'].shift(1)
df['ma5'] = df['Close'].rolling(window=5).mean()
df.dropna(inplace=True)

X = df[['lag1', 'ma5']]
y = df['Close']

# 2. GridSearchCV 설정
param_grid = {
    'n_estimators': [100, 300, 500],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7],
    'subsample': [0.8, 1.0]
}

tscv = TimeSeriesSplit(n_splits=3)
model = XGBRegressor(n_jobs=-1, random_state=42)

grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=tscv,
    scoring='neg_mean_absolute_error',
    verbose=1
)

grid_search.fit(X, y)

# 3. 결과 데이터 정리
results = pd.DataFrame(grid_search.cv_results_)
results['MAE'] = -results['mean_test_score']

# 4. 시각화 (Seaborn 없이 Matplotlib만 사용)
params_to_plot = ['n_estimators', 'learning_rate', 'max_depth', 'subsample']
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for i, param in enumerate(params_to_plot):
    # 각 파라미터별로 MAE 평균값 계산 (groupby 사용)
    param_column = f'param_{param}'
    performance = results.groupby(param_column)['MAE'].mean()
    
    # 그래프 그리기
    axes[i].plot(performance.index.astype(str), performance.values, marker='o', linestyle='-', color='firebrick')
    axes[i].set_title(f'Performance by {param}', fontsize=12, fontweight='bold')
    axes[i].set_xlabel(param)
    axes[i].set_ylabel('Mean MAE')
    axes[i].grid(True, alpha=0.3)

plt.suptitle('Hyperparameter Analysis (SK Hynix)', fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# 5. 최적 결과 요약
print("\n" + "="*40)
print(f"🏆 최적 파라미터: {grid_search.best_params_}")
print(f"📉 최소 MAE (검증 데이터): {results['MAE'].min():.2f}")
print("="*40)

'''
Fitting 3 folds for each of 54 candidates, totalling 162 fits

-> 그래프 생성: 5.result_gridSearchCV3.png

========================================
🏆 최적 파라미터: {'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 100, 'subsample': 1.0}
📉 최소 MAE (검증 데이터): 58535.87
========================================
'''

