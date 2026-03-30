# 1️. 라이브러리 import

import os  # 환경변수 설정 및 OS 관련 기능 사용
import gradio as gr  # 웹 UI 생성을 위한 라이브러리
from transformers import pipeline  # Hugging Face 모델 실행용 pipeline
import torch  # PyTorch (GPU 사용 및 모델 실행)

# 2️. TensorFlow 비활성화 (충돌 방지)

# transformers가 TensorFlow를 로드하지 못하도록 설정 (PyTorch만 사용)
os.environ["TRANSFORMERS_NO_TF"] = "1"

# 3️. 디바이스 설정 (GPU / CPU 선택)

# CUDA(GPU)가 가능하면 GPU 사용(0), 아니면 CPU 사용(-1)
device = 0 if torch.cuda.is_available() else -1

# 4️. 다중 감정 분석 모델 로드

classifier = pipeline(
    task="text-classification",  #  감정 분석 → 텍스트 분류로 변경 (다중 클래스)
    model="j-hartmann/emotion-english-distilroberta-base",  #  다중 감정 모델
    framework="pt",  # PyTorch 강제 사용
    device=device,  # GPU 또는 CPU 적용
    return_all_scores=True  # 모든 감정 확률 반환 (핵심 옵션)
)

# 5️. 감정 분석 함수

def analyze_emotion(text):

    # 입력값이 공백일 경우 예외 처리
    if not text.strip():
        return "문장을 입력해주세요.", None

    # 모델 실행 (결과는 여러 감정 리스트 형태로 반환됨)
    results = classifier(text)

    # 결과 구조:
    # [[{'label': 'joy', 'score': 0.9}, {'label': 'sadness', 'score': 0.1}, ...]]

    emotion_scores = results[0]  # 첫 번째 문장 결과 추출

    # 가장 높은 확률의 감정 찾기
    top_emotion = max(emotion_scores, key=lambda x: x["score"])

    # 최고 감정 라벨과 확률 추출
    label = top_emotion["label"]
    score = top_emotion["score"]

    # Gradio Label에 맞는 형태로 변환 (딕셔너리)
    probability_dict = {
        item["label"]: float(item["score"]) for item in emotion_scores
    }

    # 사용자에게 보여줄 결과 텍스트 생성
    result_text = f"감정 결과: {label} (신뢰도: {score:.4f})"

    # 결과 텍스트 + 전체 감정 확률 반환
    return result_text, probability_dict

# 6️. Gradio UI 구성

with gr.Blocks() as demo:  # Gradio 앱 시작

    gr.Markdown("# 📊 다중 감정 분석 웹 서비스")  # 제목
    gr.Markdown("문장을 입력하면 여러 감정을 분석하고 확률을 보여줍니다.")  # 설명

    # 사용자 입력창
    input_text = gr.Textbox(
        label="입력 문장",  # 입력 라벨
        placeholder="예: I feel amazing today!",  # 입력 예시
        lines=3  # 입력창 크기
    )

    # 분석 버튼
    analyze_button = gr.Button("분석하기")

    # 결과 텍스트 출력창
    output_text = gr.Textbox(
        label="분석 결과",
        interactive=False  # 수정 불가
    )

    # 감정 확률 시각화 (자동 그래프)
    output_label = gr.Label(label="감정 확률")

    # 버튼 클릭 시 실행 연결
    analyze_button.click(
        fn=analyze_emotion,  # 실행 함수
        inputs=input_text,  # 입력값
        outputs=[output_text, output_label]  # 출력값
    )

# 7️. 서버 실행

if __name__ == "__main__":  # 현재 파일 실행 시

    # Gradio 서버 실행 (로컬 환경)
    demo.launch(
        server_name="127.0.0.1",  # 로컬호스트
        server_port=7860  # 포트 번호
    )