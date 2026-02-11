# 1. import
from sentence_transformers import SentenceTransformer # 멀티 모달 임베딩 모델 로드
from PIL import Image   # 이미지 파일 로드
import faiss            # 벡터 검색 라이브러리
import numpy as np      # 넘파이 모듈, 배열 변환용 (FAISS 필수)
import os

# 2. 작업 디렉토리
os.chdir("C:/workAI/work/LangChain/4.Multi-Modal-RAG") # -> \를 /로 변경

# 3. 멀티모달 모델 로드
model = SentenceTransformer("clip-Vit-B-32")

# 4. 이미지 파일 로드
image = Image.open("./images/cat.jpg").convert("RGB")

# 5. 이미지 -> 벡터 변환
vector = model.encode([image]) # 반드시 리스트 형태로 넣어서 (1,512) 배치 형태로 생성(정수)

# FAISS는 float32 타입만 허용
vector = vector.astype("float32")

# 6. FAISS 인덱스 생성 => 데이터가 많을 때 북마크 역할(정렬(ㄱ~ㅎ))
dimension = vector.shape[1] # 모델 출력 차원 자동 추출 (512)
index = faiss.IndexFlatL2(dimension) # L2 => 거리 기반 인덱스 생성
# 데이터 추가
index.add(vector) # numpy 배열를 인덱스에 추가

# 저장 확인 출력
print(f"벡터 차원: {dimension}")
print(f"인덱스에 추가된 데이터 개수: {index.ntotal}")
print("정상적으로 저장 완료!")

'''
벡터 차원: 512
인덱스에 추가된 데이터 개수: 1
정상적으로 저장 완료!
'''
