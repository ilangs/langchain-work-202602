# 3.voicetest.py

# ==============================
# 1. 라이브러리
# ==============================
import gradio as gr          # Gradio 라이브러리: 웹 UI를 쉽게 만들 수 있게 해줌
import torch                 # PyTorch 라이브러리: GPU/CPU 장치 확인 및 모델 실행에 사용
from transformers import pipeline  # Hugging Face의 pipeline: STT, 번역 등 다양한 모델을 쉽게 불러올 수 있음
from gtts import gTTS        # Google Text-to-Speech: 텍스트를 음성(mp3)으로 변환
import tempfile              # 임시 파일을 생성하기 위한 라이브러리


# ==============================
# 2. 모델 설정
# ==============================

device = 0 if torch.cuda.is_available() else -1  # GPU가 있으면 0번 장치 사용, 없으면 CPU(-1) 사용

# STT (Whisper)
stt = pipeline(
    "automatic-speech-recognition",   # 음성 → 텍스트 변환 파이프라인
    model="openai/whisper-base",      # Whisper-base 모델 사용
    device=device                     # GPU 또는 CPU 장치 지정
)

# 번역 (영어 → 한국어, M2M100)
translator = pipeline(
    "translation",                    # 번역 파이프라인
    model="facebook/m2m100_418M",     # 영어→한국어 번역 지원하는 M2M100 모델
    device=device                     # GPU 또는 CPU 장치 지정
)

# ==============================
# 3. 핵심 함수
# ==============================

def process(audio):                   # 오디오 입력을 처리하는 함수
    if audio is None:                 # 입력이 없으면
        return "", "", None           # 빈 값 반환

    # 1. 음성 → 영어 텍스트
    result = stt(audio)               # Whisper로 음성을 텍스트로 변환
    text_en = result.get("text", "")  # 결과에서 텍스트 추출

    if not text_en.strip():           # 텍스트가 비어 있으면
        return "", "", None           # 빈 값 반환

    # 2. 영어 → 한국어 번역
    translated = translator(text_en, src_lang="en", tgt_lang="ko")  # 영어를 한국어로 번역
    text_ko = translated[0]["translation_text"]                     # 번역된 텍스트 추출

    # 3. 한국어 텍스트 → 음성 변환
    tts = gTTS(text=text_ko, lang="ko")                             # 한국어 텍스트를 음성으로 변환
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") # 임시 mp3 파일 생성
    tts.save(file.name)                                             # 변환된 음성을 파일로 저장

    # 결과 텍스트 + 감정 확률 + 생성된 음성파일 경로 반환
    return text_en, text_ko, file.name  # 영어 텍스트, 한국어 번역, 한국어 음성 파일 반환


# ==============================
# 4. UI
# ==============================

with gr.Blocks() as demo:             # Gradio Blocks로 UI 구성
    gr.Markdown("## 🎤 영어 음성 → 한국어 번역 + TTS")  # 제목 표시

    audio_in = gr.Audio(sources=["microphone", "upload"], type="filepath") # 오디오 입력 (마이크/업로드)
    btn = gr.Button("변환")          

    text_out_en = gr.Textbox(label="영어 텍스트 결과")   # 영어 텍스트 출력 박스
    text_out_ko = gr.Textbox(label="한국어 번역 결과")   # 한국어 번역 출력 박스
    audio_out = gr.Audio(label="한국어 음성")            # 한국어 음성 출력 박스

    btn.click(process, audio_in, [text_out_en, text_out_ko, audio_out])  # 배치순서

# ==============================
# 5. 실행
# ==============================

if __name__ == "__main__":            # 프로그램 실행 진입점
    demo.launch(inbrowser=True)       # 웹 브라우저에서 Gradio UI 실행