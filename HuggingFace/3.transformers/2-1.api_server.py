# 💻 1단계: FastAPI 서버 코드 (s4.api_server.py)
# 학습된 모델을 불러와서 항시 대기하다가, 화면(Streamlit)에서 텍스트를 보내면 스팸 여부를 판별해서 돌려주는 백엔드 API 서버

import os
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# 1. FastAPI 앱 생성
app = FastAPI(title="스팸 판별 API 서버")

# 2. 전역 변수로 모델 로드 (서버가 켜질 때 딱 한 번만 로드해서 속도 최적화)
base_dir = os.path.dirname(os.path.abspath(__file__))
# 💡 주의: 앞서 학습 완료된 폴더명을 정확히 입력하세요. (예: 500개로 학습했다면 500)
model_path = os.path.join(base_dir, "my_spam_model_500_klue")

print("[INFO] AI 모델을 서버 메모리에 로드 중입니다...")
spam_classifier = pipeline("text-classification", model=model_path, tokenizer=model_path)
print("[SUCCESS] API 서버 로딩 완료!")

# 3. 클라이언트(화면)로부터 받을 데이터 형식 정의
class MessageRequest(BaseModel):
    text: str

# 4. 판별 요청을 받는 API 엔드포인트 생성 (POST 방식)
@app.post("/predict")
def predict_spam(request: MessageRequest):
    # 입력받은 텍스트를 모델에 넣고 결과 추출
    result = spam_classifier(request.text)[0]
    
    # 결과 포맷팅
    is_spam = result["label"] == "SPAM"
    confidence = round(result["score"] * 100, 1)
    
    # 화면(Streamlit)으로 결과 JSON 반환
    return {
        "text": request.text,
        "is_spam": is_spam,
        "confidence": confidence,
        "label_name": "스팸(Spam)" if is_spam else "정상(Ham)"
    }
