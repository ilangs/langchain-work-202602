from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import joblib
#추가
import os

# FastAPI 앱 생성
app = FastAPI(title="금융 스팸 탐지 API", description="실시간 금융 스팸 문장 분류 서비스", version="1.0")

# 학습된 모델 불러오기
# 현재 작업 디렉토리 확인
current_dir = os.getcwd()
print("현재 디렉토리:", current_dir)

# 현재 디렉토리에 있는 finance_spam_model.pkl 파일 경로 생성
model_path = os.path.join(current_dir, "finance_spam_model.pkl")

# 모델 불러오기
model = joblib.load(model_path)

#model = joblib.load("finance_spam_model.pkl")

# 기본 루트: 입력 폼 제공
@app.get("/", response_class=HTMLResponse)
def form_ui():
    return """
    <html>
        <head>
            <title>금융 스팸 탐지기</title>
        </head>
        <body>
            <h2>금융 스팸 탐지기</h2>
            <form action="/predict" method="post">
                <label>문장을 입력하세요:</label><br>
                <input type="text" name="text" style="width:400px"/><br><br>
                <input type="submit" value="분석하기"/>
            </form>
        </body>
    </html>
    """

# POST 요청: 입력값 받아서 결과 반환
@app.post("/predict", response_class=HTMLResponse)
def predict_spam(text: str = Form(...)):
    pred = model.predict([text])[0]
    label = "스팸 🚨" if pred == 1 else "정상 ✅"
    return f"""
    <html>
        <head><title>분석 결과</title></head>
        <body>
            <h2>분석 결과</h2>
            <p><b>입력 문장:</b> {text}</p>
            <p><b>예측 결과:</b> {label}</p>
            <br>
            <a href="/">다시 입력하기</a>
        </body>
    </html>
    """
