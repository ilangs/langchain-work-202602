import whisper  # openai-whisper 라이브러리
import os

# 1. 모델 로드
model = whisper.load_model("base")
# 대문자 변수 => 파일 경로, 전체 소스코드에서 자주 사용되는 상수값을 저장할 목적 (=정적 변수명)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 절대경로의 파일 위치 -> 폴더명을 반환

# 2. 파일 로드
audio_path = os.path.join(BASE_DIR, "audio", "1.mp3")
print(f"\n파일 경로: {audio_path}\n")

# 3. 음성 -> 텍스트로 변환 -> AI로 전달 -> AI 응답
result = model.transcribe(audio_path, fp16=False)
print(result["text"].strip())

'''
파일 경로: c:\workAI\work\LangChain\4.Multi-Modal-RAG\audio\1.mp3

 Number one, which of the following descriptions of the image is incorrect? One, a lot of people are using laptops. Two, there are many lights installed on the ceiling. Three, the text, dive 2024 and Busan is visible. Four, people are mostly engaged in outdoor activities.
 '''