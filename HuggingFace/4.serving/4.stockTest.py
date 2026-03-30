# Streamlit 웹 UI 라이브러리 임포트 (웹 화면 구성용)
from sklearn.model_selection import learning_curve
import streamlit as st

# 한국 및 해외 주식 데이터를 가져오기 위한 라이브러리 임포트
import FinanceDataReader as fdr

# 데이터 프레임 처리 및 조작을 위한 pandas 라이브러리 임포트
import pandas as pd

# 날짜 및 시간 계산을 위한 파이썬 표준 라이브러리 임포트
import datetime

# 머신러닝 알고리즘인 XGBoost의 회귀 모델(Regressor) 임포트
from xgboost import XGBRegressor   # 수치 예측(시계열 데이터 분석)

# 대화형 그래프(시각화) 생성을 위한 Plotly 라이브러리 임포트
import plotly.graph_objects as go


# 1. 페이지 설정 단계
# 웹 브라우저 탭에 표시될 제목과 화면 레이아웃(wide: 넓게) 설정
st.set_page_config(page_title="국내 IT 대장주 AI 예측 (XGBoost)", layout="wide") 

# 메인 화면에 큰 제목 출력
st.title("🔋 삼성전자 & SK하이닉스 AI 주가 예측 (XGBoost)") 

# 오늘 날짜를 'YYYY-MM-DD' 형식의 문자열로 생성
today_str = datetime.datetime.today().strftime("%Y-%m-%d") 
# 파란색 정보 박스 안에 현재 분석 기준일 출력
st.info(f"현재 분석 기준 날짜: {today_str}") 


# 2. 사이드바(왼쪽 메뉴) 설정 단계
st.sidebar.header("🏢 종목 및 예측 설정") 

# 화면에 표시될 이름과 실제 종목 코드를 매핑한 딕셔너리 객체
stock_dict = {
    "삼성전자": "005930",   # 삼성전자 종목 코드
    "SK하이닉스": "000660"  # SK하이닉스 종목 코드
}

# 사이드바에 드롭다운 선택 상자 생성 (기본값으로 딕셔너리의 키 값들 표시)
selected_name = st.sidebar.selectbox(
    "예측할 종목을 선택하세요",   
    list(stock_dict.keys())
)

# 사용자가 선택한 종목 이름에 해당하는 종목 코드 추출
target_ticker = stock_dict[selected_name]

# 슬라이더를 통해 미래를 몇 일 동안 예측할지 설정 (7일~90일 사이, 기본 30일)
period = st.sidebar.slider("미래 예측 기간", 7, 90, 30) 


# 3. 데이터 로드 함수 정의
# @st.cache_data: 데이터를 매번 새로 받지 않고 600초 동안 메모리에 보관(속도 향상)
@st.cache_data(ttl=600)  
def load_data(ticker):

    try:
        # 분석을 시작할 기준 날짜 설정
        start_date = "2020-01-01"

        # 데이터 수집 종료 날짜 (오늘)
        end_date = datetime.datetime.today().strftime("%Y-%m-%d")

        # FinanceDataReader를 사용하여 주가 데이터 다운로드
        df = fdr.DataReader(ticker, start_date, end_date)

        # 만약 데이터가 비어있다면 한국거래소(KRX) 접두사를 붙여 재시도
        if df is None or df.empty:
            df = fdr.DataReader(f"KRX:{ticker}", start_date, end_date)

        # 여전히 데이터가 없으면 None 반환
        if df is None or df.empty:
            return None

        # 날짜가 인덱스로 되어 있는데, 이를 분석하기 편하게 일반 컬럼으로 변환
        df.reset_index(inplace=True)

        return df

    except:
        # 에러 발생 시 None 반환
        return None


# 작성한 함수를 호출하여 주가 데이터를 가져옴
data = load_data(target_ticker)


# 데이터를 성공적으로 불러온 경우에만 아래 로직 실행
if data is not None and not data.empty:

    # 상태 진행 바 표시 (분석이 끝날 때까지 유지)
    with st.status(f"{selected_name} 분석 중..."): 

        # ----------------------------------
        # 4. 특성 공학 (Feature Engineering)
        #  모델이 학습하기 쉽게 특정한 속성을 뽑아내는 작업 
        #  감정분석 -> 기분이 좋다->숫자로 변환->긍정/부정
        #  구매분석 -> 20,27,30,,,->나이->20대,30대,40대,,,=>분리->모델 훈련    
        # ----------------------------------
        # 모델이 학습하기 좋게 날짜 데이터에서 추가 정보를 추출함

        df = data.copy()  # 복사본으로 작업하겠다는 표시

        # 'Date' 컬럼에서 일, 월, 년, 요일 정보를 숫자로 추출하여 새 컬럼 생성
        df['day'] = df['Date'].dt.day
        df['month'] = df['Date'].dt.month
        df['year'] = df['Date'].dt.year
        df['weekday'] = df['Date'].dt.weekday

        # Lag Feature: 과거의 주가 정보를 입력값으로 사용 (1일 전, 2일 전, 3일 전 종가)
        df['lag1'] = df['Close'].shift(1)
        df['lag2'] = df['Close'].shift(2)
        df['lag3'] = df['Close'].shift(3)

        # 과거 데이터가 없는 초기 행(NaN)들은 제거
        df.dropna(inplace=True)

        # 머신러닝 모델의 입력 변수(X)와 맞추고자 하는 정답값(y, 종가) 분리
        X = df[['day','month','year','weekday','lag1','lag2','lag3']] # 입력변수
        y = df['Close'] # 결과변수

        # -----------------------------
        # 5. XGBoost 모델 설정 및 학습
        # -----------------------------
        model = XGBRegressor(    # 하이퍼파라미터 작업 => 모델에게 임의의 값을 부여해서 학습시키는 것
            n_estimators=300,    # 생성할 의사결정 나무의 갯수(=모델이 반복할 횟수)
            learning_rate=0.05,  # 학습속도 조절 파라미터 값
            max_depth=5,         # 각 나무의 최대 깊이 (=복잡도 제한)
        )
        
        # 준비된 학습 데이터(X)와 정답(y)으로 모델 학습 시작
        model.fit(X, y)
        
        # --------------------------------------------
        # 6. 미래 주가 반복 예측 (Recursive Forecasting)
        # --------------------------------------------

        # 가장 최신 날짜의 데이터를 가져와서 예측의 시작점으로 설정
        last_row = df.iloc[-1] 

        future_preds = []               # 예측된 날짜와 가격을 저장할 리스트
        current_input = last_row.copy() # 루프를 돌며 업데이트할 현재 데이터 상태

        for i in range(period): # 사용자가 설정한 기간만큼 반복

            # 현재 날짜에 하루를 더함
            next_date = current_input['Date'] + datetime.timedelta(days=1)

            # 모델의 입력 형식에 맞게 새로운 특성 생성
            new_data = {
                'day': next_date.day,
                'month': next_date.month,
                'year': next_date.year,
                'weekday': next_date.weekday(),
                'lag1': current_input['Close'], # 어제의 주가(방금 예측한 값 혹은 실제 마지막 값)
                'lag2': current_input['lag1'],  # 2일전 주가
                'lag3': current_input['lag2'],  # 3일전 주가
            }

            # 딕셔너리를 모델 입력용 데이터프레임으로 변환
            X_pred = pd.DataFrame([new_data])
            
            # 학습된 모델을 사용하여 다음 날의 주가 예측
            y_pred = model.predict(X_pred)[0]

            # 결과 리스트에 날짜와 예측된 가격 저장
            future_preds.append((next_date,y_pred))

            # 다음 루프(다음 날) 예측을 위해 입력값 업데이트
            current_input['Date'] = next_date
            current_input['Close'] = y_pred
            current_input['lag1'] = new_data['lag1']
            current_input['lag2'] = new_data['lag2']
            
        # 반복문 종료 후 예측 결과 리스트를 데이터프레임으로 변환
        future_df = pd.DataFrame(future_preds, columns=['Date', 'Predicted'])

        # ---------------------
        # 7. 결과 시각화 및 출력
        # ---------------------

        # 화면 레이아웃을 2:1 비율의 두 컬럼으로 나눔
        col1, col2 = st.columns([2, 1]) 

        with col1:
            # 왼쪽 컬럼: 주가 추이 그래프 출력
            st.subheader(f"📈 {selected_name} 주가 예측")

            fig = go.Figure()

            # 실제 과거 데이터 선 그래프 추가
            fig.add_trace(go.Scatter(
                x=data['Date'],
                y=data['Close'],
                name='실제 주가'
            ))

            # AI가 예측한 미래 데이터 선 그래프 추가
            fig.add_trace(go.Scatter(
                x=future_df['Date'],
                y=future_df['Predicted'],
                name='예측 주가',
                line=dict(dash='dash') # 예측선은 점선으로 표시
            ))

            # Plotly 그래프를 Streamlit 화면에 꽉 차게 출력
            st.plotly_chart(fig, width='stretch')

        with col2:
            # 오른쪽 컬럼: 주요 수치 및 데이터 표 출력
            st.subheader("📋 예측 결과")

            # 예측 기간 중 마지막 날의 정보 추출
            last_price = future_df.iloc[-1] 

            # 지표(Metric) 위젯으로 마지막 예측일의 예상 가격 표시
            st.metric(
                label=f"{last_price['Date'].strftime('%Y-%m-%d')} 예상가", 
                value=f"₩{int(last_price['Predicted']):,}" # 천 단위 콤마 포맷팅
            )

            # 예측 데이터프레임의 마지막 10개 행을 표로 표시
            st.dataframe(future_df.tail(10)) 

else:
    # 데이터 로드에 실패했거나 데이터가 존재하지 않을 경우 에러 메시지 출력
    st.error("📉 데이터를 불러오지 못했습니다. 종목 코드나 인터넷 연결을 확인하세요.")