# 11.moviePredict.py 파일 작성

import torch                             # 파이토치 임포트
from transformers import AutoTokenizer, AutoModelForSequenceClassification
# 토크나이저와 모델 로더 임포트
import torch.nn.functional as F          # 확률 계산을 위한 소프트맥스 함수용 임포트
import os

# 1. 저장된 모델과 토크나이저 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "data", "my_movie_model_500")  # 훈련시킨 모델
base_model = "bert-base-multilingual-cased"      # 원본 베이스 모델 이름

# 2. 모델 및 토크나이저 불러오기
# 학습된 가중치가 담긴 모델을 로드합니다.
tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# 3. 모델을 평가 모드로 전환 (학습 기능 비활성화)
model.eval()

def predict_sentiment(text):
    """문장을 입력받아 긍정/부정 결과를 반환하는 함수"""
    
    # 4. 입력 문장 토큰화 (return_tensors="pt"-> 텐서형태로 변환)
    # 학습 때와 동일하게 truncation과 padding 설정을 적용합니다.
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=64)
    
    # 5. 모델 예측 실행
    with torch.no_grad():             # 예측시에는 기울기 계산 필요 없음 (메모리 절약)
        outputs = model(**inputs)     # 모델에 입력 전달한 후에 결과 반환
    
    # 6. 결과 해석 (Logits -> Softmax 확률 변환)
    logits = outputs.logits             # 모델 출력의 로짓값(=각 클래스(부정,긍정)에 대한 점수)
    probs = F.softmax(logits, dim=-1)   # 소프트맥스로 각 클래스 값의 확률 계산
    
    # 가장 높은 확률을 가진 인덱스 추출 (0 또는 1)
    prediction = torch.argmax(probs, dim=-1).item() # 가장 확룰이 높은 값의 클래스 인덱스 선택
    conf = torch.max(probs).item() * 100            # 확신도(%) 계산
    
    # 결과 출력
    sentiment = "긍정 (Positive)" if prediction == 1 else "부정 (Negative)"
    print(f"\n입력 문장: {text}")
    print(f"분석 결과: {sentiment} ({conf:.2f}% 확신)")

# 7. 테스트 실행
if __name__ == "__main__":    # 현재 파일에서 함수를 호출했는지를 체크
    print("--- 영화 리뷰 감성 분석기 ---")
    
    while True :
        # 직접 입력해서 테스트하기
        test_text = input("\n분석할 리뷰를 입력하세요(종료 exit 입력): ")
        predict_sentiment(test_text)
        
        if test_text == "exit":
            print("프로그램을 종료합니다.")
            break
        
    # 예시 문장들 테스트
    # predict_sentiment("이건 진짜 내 인생 영화다.. 너무 감동이야.")
    # predict_sentiment("중간에 잠들 뻔했어요. 전개가 너무 느림.")
