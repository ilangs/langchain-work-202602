# 1️. 라이브러리 import

import os  # 운영체제 관련 기능 사용 (환경변수 설정, 파일 경로 처리 등)
import gradio as gr  # 웹 UI를 쉽게 만들기 위한 라이브러리
from transformers import pipeline  # Hugging Face 모델을 간편하게 사용하기 위한 함수
import torch  # PyTorch (딥러닝 모델 실행 및 GPU 사용)
from gtts import gTTS  # 텍스트를 음성(mp3)으로 변환하는 라이브러리
import uuid  # 고유한 파일명을 생성하기 위한 라이브러리 (파일 충돌 방지)

# 2️. TensorFlow 비활성화

os.environ["TRANSFORMERS_NO_TF"] = "1"  
# transformers 라이브러리가 TensorFlow를 자동으로 로드하지 못하도록 설정 (PyTorch만 사용)

# 3️. 디바이스 설정

device = 0 if torch.cuda.is_available() else -1  
# GPU(CUDA)가 있으면 0번 GPU 사용, 없으면 CPU(-1) 사용

# 4️. 다중 감정 모델 로드

classifier = pipeline(
    task="text-classification",  # 텍스트를 여러 감정 클래스로 분류하는 작업
    model="j-hartmann/emotion-english-distilroberta-base",  # 다중 감정 분석 모델
    framework="pt",  # PyTorch 기반으로 모델 실행
    device=device,  # GPU 또는 CPU 설정 적용
    return_all_scores=True  # 모든 감정의 확률을 반환 (핵심 옵션)
)

# 5️. 감정 분석 + 음성 생성 함수

def analyze_emotion_with_tts(text):

    # 입력값이 공백이면 실행하지 않도록 처리
    if not text.strip():
        return "문장을 입력해주세요.", None, None

    # 입력 텍스트를 모델에 넣어 감정 분석 수행
    results = classifier(text)

    # 결과 구조: [[{label: 감정, score: 확률}, ...]]
    emotion_scores = results[0]  # 첫 번째 문장 결과 추출

    # 가장 높은 확률을 가진 감정 선택
    top_emotion = max(emotion_scores, key=lambda x: x["score"])

    # 선택된 감정 라벨과 확률 저장
    label = top_emotion["label"]
    score = top_emotion["score"]

    # Gradio Label 컴포넌트에 전달할 확률 딕셔너리 생성
    probability_dict = {
        item["label"]: float(item["score"]) for item in emotion_scores
    }

    # 사용자에게 보여줄 결과 문자열 생성
    result_text = f"Emotion: {label} (confidence: {score:.4f})"

    # TTS(Text-to-Speech) 음성 생성
    tts = gTTS(text=text, lang='en') # 입력 텍스트를 영어 음성으로 변환

    # 고유한 파일명 생성 (파일 덮어쓰기 방지)
    filename = f"output_{uuid.uuid4().hex}.mp3"  # uuid를 사용해 랜덤한 파일명 생성

    # 음성 파일 저장
    tts.save(filename)  # mp3 파일로 저장

    # 결과 텍스트 + 감정 확률 + 생성된 음성 파일 경로 반환
    return result_text, probability_dict, filename

# 6️. Gradio UI 구성

with gr.Blocks() as demo:  # Gradio UI 블록 시작

    gr.Markdown("# 📊 다중 감정 분석 + 음성 생성 서비스")  # 웹 페이지 제목 출력

    gr.Markdown("문장을 입력하면 감정을 분석하고 음성 파일을 생성합니다.")  # 서비스 설명 문구

    # 사용자 입력 텍스트 박스 생성
    input_text = gr.Textbox(
        label="입력 문장",  # 입력창 라벨
        placeholder="예: I feel amazing today!",  # 예시 문장
        lines=3  # 입력창 높이
    )

    # 분석 실행 버튼 생성
    analyze_button = gr.Button("분석 + 음성 생성")

    # 감정 분석 결과를 출력할 텍스트 박스
    output_text = gr.Textbox(label="감정 분석 결과")

    # 감정 확률을 시각화하는 Label 컴포넌트
    output_label = gr.Label(label="감정 확률")

    # 생성된 음성을 재생 및 다운로드할 Audio 컴포넌트
    # type="filepath" → 파일 경로를 받아서 자동으로 플레이 + 다운로드 제공
    audio_output = gr.Audio(label="생성된 음성", type="filepath")
    
    # 버튼 클릭 시 실행될 함수 연결
    analyze_button.click(
        fn=analyze_emotion_with_tts,  # 실행 함수
        inputs=input_text,  # 입력 데이터
        outputs=[output_text, output_label, audio_output]  # 출력 데이터
    )

# 7️. 서버 실행

if __name__ == "__main__":  # 현재 파일을 직접 실행할 경우만 동작

    demo.launch(
        server_name="127.0.0.1",  # 로컬 서버 주소
        server_port=7860  # 포트 번호
    )