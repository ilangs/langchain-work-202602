# 1. import
from sentence_transformers import SentenceTransformer # 멀티 모달 임베딩 모델 로드 (텍스트,이미지+벡터)
from PIL import Image   # 이미지 파일 로드
import faiss            # 벡터 검색 라이브러리
import numpy as np      # 넘파이 모듈, 배열 변환용 (FAISS 필수)
import os

# 2. 작업 디렉토리
os.chdir("C:/workAI/work/LangChain/4.Multi-Modal-RAG") # -> \를 /로 변경
print(f"현재 위치: {os.getcwd()}")  # 현재 위치 확인 점검

# 3. 멀티모달 모델 로드
model = SentenceTransformer("clip-Vit-B-32")

# 4. 멀티 이미지 파일 로드
##############################################################################################
image_paths = ["./images/cat.jpg", 
               "./images/dog.png", 
               "./images/car.png" ]

images = []
for path in image_paths:
    img = Image.open(path).convert("RGB")
    images.append(img)

# images = [Image.open(path).convert("RGB") for path in image_paths]    # 축약형
    
# # 실무형 안전한 코드
# images = []
# for path in image_paths:
#     try:
#         img = Image.open(path).convert("RGB")
#         images.append(img)
#     except Exception as e:
#         print(f"파일 로드 실패: {path} - 이유: {e}")
#         # 실패한 이미지는 건너뛰고 다음 파일 진행


# 5. 이미지 -> 벡터 변환
image_vector = model.encode(images) # 반드시 리스트 형태 입력 필수인데, images 자체가 List 객체임

# FAISS는 float32 타입만 허용
image_vector = image_vector.astype("float32") # 실수 형태로 반환 (검색 정확도 향상) 예) 5 => 5.767 

##############################################################################################
# 6. FAISS 인덱스 생성 => 데이터가 많을 때 북마크 역할(정렬(ㄱ~ㅎ))
dimension = image_vector.shape[1] # 모델 출력 차원 자동 추출 (512)
index = faiss.IndexFlatL2(dimension) # L2 => 거리 기반 인덱스 생성
# 데이터 추가
index.add(image_vector) # numpy 배열를 인덱스에 추가

# 7. 텍스트 => 벡터 변환
query = "a running dog"
# 객체명.호출할메서드명().메서드명()~ Chainning method 방법
query_vector = model.encode([query]).astype("float32") # 반드시 리스트 형태 입력, 벡터(숫자) => 실수 반환
# query_vector = query_vector.astype("float32") 

# 8. 유사도 벡터 검색
distances, indices = index.search(query_vector, k=1) # k=1 => 상위 1개의 유사 검색 결과를 반환

# 저장 확인 출력
print("가장 유사한 이미지:", image_paths[indices[0][0]]) # 배열로 생각 (가장 가까운 이미지)
print("거리값:", distances[0][0])


'''
현재 위치: C:\workAI\work\LangChain\4.Multi-Modal-RAG
가장 유사한 이미지: ./images/dog.png
거리값: 149.92932
'''


'''
[ 참고 사항 ]

실무에서 유사도(Similarity) 값을 높이고 변별력을 확보한다는 것은 결국 "수많은 데이터 중에서 내가 원하는 정답만 정확하게 골라내겠다"는 의지이자, RAG 시스템의 품질을 결정짓는 핵심 요소입니다.

단순히 검색이 되는 것을 넘어, 실무에서 검색의 질을 비약적으로 높일 수 있는 3가지 핵심 전략을 정리해 드립니다.

1. 임베딩 모델의 고도화 (The Core)
현재 사용하시는 clip-Vit-B-32는 매우 훌륭한 범용 모델이지만, 특정 도메인(예: 의료, 패션, 부품, 퀼트 등)에서는 한계가 있을 수 있습니다.

1) Fine-tuning: 수집하신 특정 이미지 데이터를 모델에게 추가 학습시켜 "우리 회사만의 고유한 특징"을 이해하게 만듭니다.

2) 최신/대형 모델 사용: ViT-L-14나 ViT-H-14처럼 파라미터 수가 더 많은 상위 모델을 쓰면 벡터의 정밀도가 올라가 검색 질이 향상됩니다.

2. 코사인 유사도(Cosine Similarity) 활용
현재 사용하시는 IndexFlatL2는 단순히 두 점 사이의 직선 거리(유클리드 거리)를 잽니다. 하지만 이미지/텍스트 검색에서는 **벡터 간의 각도(방향성)**를 측정하는 코사인 유사도가 훨씬 정확한 경우가 많습니다.

1) 방법: 입력 벡터를 정규화(Normalization)한 뒤 IndexFlatIP(Inner Product)를 사용하면 코사인 유사도 검색이 가능해집니다.

3. 하이브리드 검색 (Multi-modal Logic)
이미지의 시각적 특징뿐만 아니라, **이미지에 붙은 태그나 설명(Text)**을 함께 검색 조건으로 활용합니다.

1) Re-ranking: FAISS로 상위 100개를 빠르게 뽑은 뒤, 더 무겁고 정교한 모델로 상위 5개를 다시 정렬하는 방식을 실무에서 가장 많이 씁니다.
'''
