# =================================================================================================
# 1. import
# =================================================================================================
import whisper          # openai-whisper 음성 라이브러리
from sentence_transformers import SentenceTransformer # 멀티 모달 임베딩 모델 로드 (텍스트,이미지+벡터)
from PIL import Image   # 이미지 파일 로드
import faiss            # 벡터 검색 라이브러리
import numpy as np      # 넘파이 모듈, 배열 변환용 (FAISS 필수)
import os

# AI 요청
from dotenv import load_dotenv
# langchain 라이브러리
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# =================================================================================================
# 2. 음성 데이터 처리 => (음성을 텍스트로 변환)
# =================================================================================================
whisper_model = whisper.load_model("base")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
audio_path = os.path.join(BASE_DIR, "audio", "cat.mp3")
# STT 처리
speech_result = whisper_model.transcribe(audio_path, fp16=False)
speech_text = speech_result["text"].strip() # 양쪽 여백 제거 "Show me the cat information"
print(f"[음성 인식 내용]: {speech_text}")

# =================================================================================================
# 3. 텍스트 모델 로드
# =================================================================================================
clip_model = SentenceTransformer("clip-Vit-B-32")

# 텍스트 기반의 지식들을 리스트 형태로 준비
documents = [
    "Information: This is a domestic cat sitting comfortably.", # 고양이에 대한 설명
    "Information: There is a golden retriever dog in the yard.", # 강아지에 대한 설명
    "Concept: AI and Machine Learning technologies.",           # AI 기술 설명
    "Concept: Retrieval-Augmented Generation (RAG) system."      # RAG 시스템 설명
]
text_vectors = clip_model.encode(documents).astype("float32") # 문장들을 512 차원 벡터로 변환

# =================================================================================================
# 4. 작업 디렉토리 
# =================================================================================================
os.chdir("C:/workAI/work/LangChain/4.Multi-Modal-RAG") # -> \를 /로 변경
print(f"os.getcwd()=> {os.getcwd()}")

# =================================================================================================
# 5. CLIP 멀티 모달 모델 로드
# =================================================================================================
image_path = "./images/cat.jpg"
img = Image.open(image_path).convert("RGB")
image_vector = clip_model.encode([img]).astype("float32")   # 이미지 -> 벡터 변환

# =================================================================================================
# 6. FAISS 인덱스 생성 => 인덱스 => 데이터가 많을 때 북마크 역할 (정렬(ㄱ~ㅎ))
# =================================================================================================
dimension = text_vectors.shape[1]    # 모델 출력 차원 자동 추출 (512)
index = faiss.IndexFlatL2(dimension) # L2 => 거리 기반 인덱스 생성
index.add(text_vectors) # 텍스트 먼저 index에 올리고,

index.add(np.array(image_vector)) # numpy float32 배열을 index에 추가 => 고속 배열 연산

# =================================================================================================
# 7. 연관 정보 찾기 (Retrieval)
# =================================================================================================
# 사용장의 음성 질문(텍스트)을 검색을 위해 숫자 벡터로 변환
query_vector = clip_model.encode([speech_text]).astype("float32")
# 질문과 가장 닮은 상위 3개의 정보을 지식창고에서 찾는다. (거리값, 변호값)
distances, indices = index.search(query_vector, k=3) 
# 검색된 결과를 사람이 읽을 수 있는 텍스트로 변환하여 담을 리스트
retrieved_contents = []
for idx in indices[0]: # 가장 최근에 찾은 값 [0]
    if idx < len(documents): # 찾은 번호가 0~3번 이면, 해당 텍스트 번호를 그대로 가져온다. 0~3 < 4
        retrieved_contents.append(documents[idx])
    elif idx == len(documents): # 찾은 번호가 4번이면, 이미지를 설명하는 텍스트로 추가한다.
        retrieved_contents.append("Visual Data: A high-resolution photo of a cat from 'cat.jpg'")
    else:
        raise ValueError(f"Unexpected index: {idx}")
    
# 찾은 정보들을 줄바꿈으로 (\n)으로 연결해해서 하나의 참고 자료로 만들기
# 파이썬은 문자열도 객체, 예) test="abc" -> test.strip() = test="abc".strip()
context_text = "\n".join(retrieved_contents)  
print(f"[검색된 연관 정보]: \n{context_text}")

# =================================================================================================
# 8. 지능형 답변 생성(Generation) => ChatGPT로 전달할 프롬프트
# =================================================================================================
prompt = ChatPromptTemplate.from_template("""
    당신은 멀티모달 정보를 처리해 주는 전문가 AI 입니다.
    제공된 [Context]에는 텍스트 정보뿐만 아니라 이미지 파일에 대한 설명(Visual Data)도 포함되어 있습니다.
    사용자의 질문인 [Question]과 가장 연관성이 높은 정보를 [Context]에서 찾아 상세히 답변해 주세요.

    [Context]:
    {context}

    [Question]:
    {question} 

    [Answer]: 
""")

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

chain = prompt | llm | StrOutputParser()

final_answer = chain.invoke({
    "context": context_text,   # 위에서 검색한 참고 자료들
    "question": speech_text    # 사용자의 원래 음성 질문
})
print("-" * 50)
print(f"[최종 답변]: \n{final_answer}")


'''
[음성 인식 내용]: Show me the cat information
os.getcwd()=> C:\workAI\work\LangChain\4.Multi-Modal-RAG
[검색된 연관 정보]: 
Information: This is a domestic cat sitting comfortably.
Concept: AI and Machine Learning technologies.
Concept: Retrieval-Augmented Generation (RAG) system.
--------------------------------------------------
[최종 답변]: 
The information provided indicates that there is a domestic cat sitting comfortably. This suggests that the cat is likely in a relaxed position, possibly enjoying its surroundings. Domestic cats are known for their playful and affectionate nature, often seeking comfort in cozy spots around the home. If you have any specific questions about the cat or need more details, feel free to ask!
'''