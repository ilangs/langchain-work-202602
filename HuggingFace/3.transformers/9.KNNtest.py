# 9.KNNtest.py

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 추가
from sklearn.neighbors import KNeighborsClassifier # KNN을 이용 (분류)
from sklearn.datasets import load_iris             # 벚꽃(150개)
from sklearn.preprocessing import StandardScaler   # 표시x (표준화)

############################################################################# 

# 1. 페이지 설정
# 웹 브라우저 탭에 표시될 제목을 설정하고, 화면 레이아웃을 넓게(wide) 지정합니다.
st.set_page_config(page_title="KNN 3D 시각화", layout="wide")
# 메인 화면에 표시될 큰 제목을 출력합니다.
st.title("🧊 KNN 3차원 공간 거리 시각화")
# 앱의 목적을 설명하는 간단한 문구를 작성합니다.
st.write("3개의 특성을 사용하여 공간상에서 가장 가까운 이웃을 찾습니다.")

# 2. 데이터 준비 (3개 특성 선택: Sepal Length, Sepal Width, Petal Length)
# 사이킷런에서 제공하는 붓꽃(Iris) 데이터셋을 불러옵니다.
iris = load_iris()
# 데이터 스케일링 (3차원 공간에서 거리 왜곡을 방지합니다)
# 특성마다 단위가 다르므로, 모든 데이터를 평균 0, 표준편차 1인 표준 정규분포로 변환합니다.
X = iris.data[:,:3] # 전체 데이터 중(:)  0,1,2
# 각 데이터의 정답 (품종:0,1,2)
y = iris.target
# 선택한 3개의 특성 이름을 따로 리스트에 저장
feature_names = iris.feature_names[:3]

# 데이터 스케일링 (3차원 공간에서 거리 왜곡) 모든 데이터를 평균 0, 표준편차 1
scaler = StandardScaler()
# 전체 대이터를 스케일러에 적합시키고 변환
X_scaled = scaler.fit_transform(X)

##################################################################################

# 3. 사이드바 입력
# 왼쪽 사이드바에 입력 섹션 제목을 표시합니다.
st.sidebar.header("📍 새로운 데이터 입력")
# 슬라이더를 통해 사용자가 테스트할 붓꽃의 수치(길이, 너비)를 직접 입력받습니다.
sl = st.sidebar.slider("Sepal Length", 4.0, 8.0, 5.8)
sw = st.sidebar.slider("Sepal Width", 2.0, 4.5, 3.0)
pl = st.sidebar.slider("Petal Length", 1.0, 7.0, 4.3)
# 분류 결정에 참고할 이웃의 수(K)를 입력받습니다 (기본값 3).
k_neighbors = st.sidebar.number_input("이웃의 수(k)",min_value=1,max_value=15,value=3)

# 4. 모델 학습 및 예측
# 사용자가 슬라이더로 입력한 값을 2차원 배열 형태로 만듭니다.
new_point = np.array([[sl,sw,pl]])
# 사용자 입력력값도 단위 일치(=스케일링(=표준화))
new_point_scaled = scaler.transform(new_point)

# k개 이웃을 하고 있는 KNN 분류기 객체 생성
knn = KNeighborsClassifier(n_neighbors=k_neighbors) # 설정한 k값
# 스케일링된 학습데이터와 정잠 정보를 모델에 학습->fit()
knn.fit(X_scaled,y)

# 입력한 점(new_point_scaled)오 가장 가까운 k개의 이웃의 거리와 해당데이터의 인덱스 값을 찾아낸다.
distances,indices = knn.kneighbors(new_point_scaled)
# 3차원(3D) 축을 생성하여 입체적인 그래프를 준비합니다.
prediction = knn.predict(new_point_scaled) # 품종

# [수정포인트] 예측된 품종 이름을 변수로 명확히 저장합니다. (아래 이미지 렌더링에서 사용)
predicted_species = iris.target_names[prediction[0]]

###################################################################################

# 5. 3D 시각화 (Matplotlib 3D)
# 그래프를 그릴 도화지(Figure) 크기를 설정합니다.
fig = plt.figure(figsize=(10, 8))
# 3차원(3d) 축을 생성하여 입체적인 그래프를 준비합니다.
ax = fig.add_subplot(111, projection='3d') 

# 기존 데이터 포인트들을 품종별로 반복문을 돌며 점(scatter)으로 그립니다.
colors = ['#1f77b4', '#ff7f0e', '#2ca02c'] # 품종별 색상 지정
for i, name in enumerate(iris.target_names):
    # 해당 품종에 속하는 데이터들만 추출하여 3차원 공간에 표시합니다.
    ax.scatter(X_scaled[y==i, 0], X_scaled[y==i, 1], X_scaled[y==i, 2], 
               label=name, alpha=0.4, s=30, c=colors[i])

# 사용자가 입력한 새로운 데이터 포인트는 빨간색 별 모양(*)으로 크게 표시합니다.
ax.scatter(new_point_scaled[0, 0], new_point_scaled[0, 1], new_point_scaled[0, 2], 
           c='red', marker='*', s=300, label='New Data', depthshade=False)

# 새로운 데이터 점과 가장 가까운 K개의 이웃들 사이에 검정색 점선을 연결(거리를 시각적으로 표시)
for idx in indices[0]:
    neighbor = X_scaled[idx] # 이웃의 좌표 정보를 가져옵니다.
    # 두 지점을 잇는 선을 그립니다 (x, y, z 좌표 리스트 전달).
    ax.plot([new_point_scaled[0, 0], neighbor[0]], 
            [new_point_scaled[0, 1], neighbor[1]], 
            [new_point_scaled[0, 2], neighbor[2]], 
            'k--', lw=1.5, alpha=0.8)

# 각 축에 어떤 특성인지 이름을 붙여줍니다.
ax.set_xlabel(feature_names[0])
ax.set_ylabel(feature_names[1])
ax.set_zlabel(feature_names[2], labelpad=10)

# 그래프 상단에 현재 설정된 K값을 포함한 제목을 출력합니다.
ax.set_title(f"KNN 3D View (K={k_neighbors})")
# 범례를 표시하여 품종별 색상을 구분하게 합니다.
ax.legend()

# [수정 1] 3D 그래프 마진 조정 (오른쪽 라벨 'Petal Length' 잘림 방지)
# Figure의 오른쪽 여백(right margin)을 줄여 그래프 전체를 상대적으로 왼쪽으로 이동시킵니다.
# 필요에 따라 right 값을 0.8 ~ 0.9 사이로 미세 조정하십시오.
fig.subplots_adjust(left=0.0, right=0.75, bottom=0.1, top=0.9)


#################################################################################

# 6. 결과 출력
# 화면을 3:1 비율의 두 열(Column)로 나눕니다.
col1, col2 = st.columns([3, 1])

with col1:
    # 왼쪽 열에는 생성한 Matplotlib 3D 그래프를 출력합니다.
    st.pyplot(fig) 

with col2:
    # 오른쪽 열에는 예측된 품종 결과를 보기 좋게 표시합니다.
    st.subheader("🔮 예측 결과")
    st.success(f"예측 품종: **{iris.target_names[prediction[0]]}**")
    
    # K개의 이웃들과의 실제 거리와 그 이웃의 품종이 무엇인지 표로 보여줍니다.
    st.subheader("📏 이웃 상세 정보")
    dist_df = pd.DataFrame({
        'Distance': distances[0].round(4), # 거리를 소수점 4자리까지 반올림
        'Species': [iris.target_names[y[i]] for i in indices[0]] # 해당 이웃의 실제 품종 이름
    })
    st.table(dist_df) # Streamlit 테이블 형태로 출력
    
    # [수정 2] 실물 이미지 출력 추가
    st.subheader("🌸 예측 품종 이미지")
    
    # 품종별 이미지 Mapping (URL 또는 Local Absolute Path)
    # Network 단절 환경(Offline)을 고려한다면 URL 대신 아래와 같이 Local Absolute Path를 권장합니다.
    # 예: "setosa": r"C:\workAI\work\HuggingFace\3.transformers\images\setosa.jpg"
    image_dict = {
        "setosa": "https://upload.wikimedia.org/wikipedia/commons/5/56/Kosaciec_szczecinkowaty_Iris_setosa.jpg",
        "versicolor": "https://upload.wikimedia.org/wikipedia/commons/4/41/Iris_versicolor_3.jpg",
        "virginica": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Iris_virginica.jpg"
    }
    
    # 해당 품종의 이미지가 존재할 경우 Streamlit 컨테이너 폭에 맞추어 렌더링
    if predicted_species in image_dict:
        st.image(
            image_dict[predicted_species], 
            caption=f"Iris {predicted_species}", 
            use_container_width=True # col2의 너비에 맞게 이미지 자동 리사이징
        )
    else:
        st.warning(f"{predicted_species}에 대한 이미지가 경로에 없습니다.")
    