# 1-1.text.py -> 1-2.text.py

# 1. 필요한 라이브러리 임포트 (가져오기)

import os  # 운영체제 시스템 설정을 제어하기 위한 라이브러리 (환경변수 설정용)
import gradio as gr  # 파이썬 코드를 웹 인터페이스(UI)로 간단히 만들어주는 라이브러리
from transformers import pipeline  # 수집->전처리->모델->전과정
import torch  # 딥러닝 프레임워크인 PyTorch (모델 연산의 핵심 엔진)

# 2. TensorFlow 비활성화 설정 (충요!)

# transformers 라이브러리가 백엔드로 TensorFlow를 찾지 않고 오직 PyTorch만 쓰도록 강제 설정
os.environ["TRANSFORMERS_NO_TF"] = "1"

# 3. 계산 장치(Device) 설정

# 시스템에 NVIDIA GPU(CUDA)가 설치되어 있으면 0번(GPU)을 사용하고, 없으면 -1(CPU)을 사용
device = 0 if torch.cuda.is_available() else -1  

# 4. 분석 모델 로드 (PyTorch 전용)

classifier = pipeline(
    task="sentiment-analysis",  # 수행할 작업 종류: 감정 분석
    model="distilbert-base-uncased-finetuned-sst-2-english",  # 사용할 사전 학습된 모델 이름 (영어 전용)
    # model="beomi/KcELECTRA-base-v2022",  # (참고) 한국어 분석을 원할 때 교체 가능한 한국어 모델
    # 한국어 구어체에 강한 koelectra 기반 미세 조정 모델
    framework="pt",  # 프레임워크를 PyTorch('pt')로 명시적으로 지정
    device=device  # 앞서 설정한 장치(GPU 또는 CPU)에서 모델 실행
)

# 5. 감정 분석 처리 함수 정의

def analyze_sentiment(text):

    # 사용자가 아무것도 입력하지 않았거나 공백만 입력했을 때의 예외 처리
    if not text.strip():  
        return "문장을 입력해주세요.", None 
    # 정상인 경우 함수는 2개의 return값 -> 예외 경우도 2개값 return -> 두번째 값 None 부여
    # -> ValueError: not enough values to unpack (expected 2, got 1) 방지 
    # 방어적 프로그래밍(Defensive Programming) 기법

    # 로드된 모델에 텍스트를 넣어 분석 실행
    result = classifier(text)  

    label = result[0]["label"]  # 모델이 예측한 감정 태그 (예: POSITIVE)
    score = result[0]["score"]  # 모델이 예측한 결과에 대한 확신도 (0.0 ~ 1.0)

    # POSITIVE(긍정)와 NEGATIVE(부정)의 확률을 각각 계산하여 시각화 준비
    if label == "POSITIVE":
        positive_score = score
        negative_score = 1 - score  # 전체 1에서 긍정 확률을 뺀 나머지를 부정 확률로 간주
    else:
        negative_score = score
        positive_score = 1 - score

    # Gradio의 Label 위젯에서 사용할 딕셔너리 형태로 저장
    probability_dict = {
        "POSITIVE": float(positive_score),
        "NEGATIVE": float(negative_score)
    }

    # 화면에 텍스트로 보여줄 결과 문자열 생성 (신뢰도는 소수점 4자리까지 표시)
    result_text = f"감정 결과: {label} (신뢰도: {score:.4f})"
    
    # 분석 텍스트 결과와 확률 데이터를 반환
    return result_text, probability_dict

# 6. Gradio 웹 UI 화면 구성

with gr.Blocks() as demo:

    # 화면 상단 제목 및 설명 출력
    gr.Markdown("# 📊 감정 분석 웹 서비스")
    gr.Markdown("문장을 입력하면 감정을 분석하고 확률을 그래프로 보여줍니다.")

    # 텍스트 입력 창 생성
    input_text = gr.Textbox(
        label="입력 문장",
        placeholder="예: I love AI!",  
        lines=3  # 입력창 높이 3줄 (줄 수)
    )

    # 분석 시작 버튼 생성
    analyze_button = gr.Button("분석하기")

    # 텍스트 결과 출력 창 생성 
    output_text = gr.Textbox(
        label="분석 결과",
        interactive=False  # 사용자 수정불가 설정 (=read only)
    )

    # 확률 분포를 막대 그래프 형태로 보여줄 레이블 생성
    output_label = gr.Label(label="감정 확률 그래프")

    # 버튼 클릭 이벤트 설정: 버튼을 누르면 analyze_sentiment 함수 실행
    analyze_button.click(
        fn=analyze_sentiment,  # 호출할 함수
        inputs=input_text,     # 함수에 들어갈 입력값 (사용자 텍스트)
        outputs=[output_text, output_label]  # 함수 결과값이 출력될 위치
    )

# 7. 웹 서버 실행

if __name__ == "__main__":
    # 로컬 호스트(127.0.0.1)의 7860 포트로 웹 서비스 시작
    demo.launch(server_name="127.0.0.1", server_port=7860)
