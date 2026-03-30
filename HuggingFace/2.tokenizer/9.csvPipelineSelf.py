# 9.csvPipelineSelf.py파일 작성
# label -> labels 컬럼명 변경: Hugging Face의 Trainer API는 내부적으로 타겟 변수명을 labels로 기대합니다. 이를 맞춰주지 않으면 Loss 계산 시 오류가 발생하므로 rename_column을 추가했습니다.
# Pandas 인덱스 찌꺼기(__index_level_0__) 제거: Dataset.from_pandas() 사용 시 간혹 기존 판다스 인덱스가 컬럼으로 딸려 들어오는 현상을 방어하는 코드를 추가했습니다.

# 입력받은 데이터 개수(data_count)를 최종 저장되는 데이터셋 폴더 이름에 동적으로 생성하도록 수정
# 300개는 my_custom_dataset_300 폴더에, 1000개는 ~_1000 폴더에 독립 캐싱 및 저장

import pandas as pd                         # 엑셀/CSV 데이터를 다루는 판다스
from datasets import Dataset, DatasetDict   # 허깅페이스 데이터셋 변환 도구
from transformers import AutoTokenizer      # 허깅페이스 자동 토크나이저 로더
import os, sys                              # 파일 경로 제어 모듈

# -------------------------------------------------------------------
# 1. 생성된 CSV 데이터 불러오기 (movie_xxx.csv)
# -------------------------------------------------------------------

# 스크립트 실행 위치 기준 절대 경로 지정 (Windows 경로 오류 방지)
base_dir = os.path.dirname(os.path.abspath(__file__))

# 불러올 데이터 개수 입력 (앞서 생성한 파일명과 일치해야 함)
try:
    data_count = input("불러올 데이터의 개수(파일명 숫자)를 입력하세요 (예: 300) : ")
    file_name = f"movie_{data_count}.csv"
    file_path = os.path.join(base_dir, "data", file_name)
except Exception as e:
    print(f"[ERROR] 입력 처리 중 오류 발생: {e}")
    sys.exit(1)

# 파일 존재 여부 확인 후 DataFrame으로 로드
if os.path.exists(file_path):
    # 생성 시 지정했던 utf-8-sig 인코딩으로 불러오기 (한글 깨짐 방지)
    df = pd.read_csv(file_path, encoding="utf-8-sig")
    print(f"[INFO] '{file_name}' 로드 완료! (총 데이터: {len(df)}개)")
    
    # 데이터 구조 확인 (디버깅용)
    print("\n[INFO] 데이터 샘플 (상위 5개):")
    print(df.head())
else:
    print(f"[ERROR] '{file_path}' 파일을 찾을 수 없습니다.")
    print("[ERROR] 8.moviecsvmake.py 스크립트를 먼저 실행하여 데이터를 생성해주세요.")
    sys.exit(1)

# -------------------------------------------------------------------
# 2. 판다스 데이터프레임을 허깅페이스 Dataset 객체로 변환
# -------------------------------------------------------------------
raw_dataset = Dataset.from_pandas(df)

# 3. 학습(Train)과 검증(Test) 데이터로 분리 (80% 학습, 20% 테스트)
# [추가] 재현성(Reproducibility)을 위해 seed=42 고정
ds_split = raw_dataset.train_test_split(test_size=0.2, seed=42)

# 4. 토크나이저 준비 (BERT 다국어 모델 기준)
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

# 5. 전처리 함수 정의
def preprocess_function(examples):
    # 'content' 컬럼을 토큰화하고, 길이를 64로 맞춥니다.
    return tokenizer(examples["content"], truncation=True, padding="max_length", max_length=64)

# 6. 전체 데이터셋에 전처리 적용 (batched=True 로 멀티스레드/배치 처리 가속)
tokenized_ds = ds_split.map(preprocess_function, batched=True)

# -------------------------------------------------------------------
# 7. 컬럼 정리 및 포맷 변환 (PyTorch / Hugging Face Trainer 호환성)
# -------------------------------------------------------------------

# [중요] 허깅페이스 Trainer는 정답 컬럼명을 'labels'로 인식하므로 이름 변경
tokenized_ds = tokenized_ds.rename_column("label", "labels")

# 학습에 불필요한 컬럼 목록 작성
cols_to_remove = ["content"]
# pandas 변환 시 딸려올 수 있는 불필요한 인덱스 컬럼 방어
if "__index_level_0__" in tokenized_ds["train"].column_names:
    cols_to_remove.append("__index_level_0__")

# 불필요한 컬럼 일괄 제거 (input_ids, attention_mask, labels, token_type_ids 등만 남김)
tokenized_ds = tokenized_ds.remove_columns(cols_to_remove)

# -------------------------------------------------------------------
# 8. 파이토치(PyTorch) 텐서 형식으로 최종 변환
# -------------------------------------------------------------------
tokenized_ds.set_format("torch")

# -------------------------------------------------------------------
# 9. 결과 확인
# -------------------------------------------------------------------
print("\n--- 커스텀 데이터셋 준비 완료 ---")
print(tokenized_ds)
print("\n첫 번째 학습 데이터 샘플 (텐서 구조 확인):\n", tokenized_ds["train"][0])

# -------------------------------------------------------------------
# 10. 로컬 디스크에 Hugging Face Dataset 형태로 캐싱/저장
# -------------------------------------------------------------------
# [수정] 입력받은 data_count를 활용하여 동적 폴더명 생성 (예: my_custom_dataset_300)
dataset_folder_name = f"my_custom_dataset_{data_count}"
dataset_path = os.path.join(base_dir, "data", dataset_folder_name)

# 오프라인 로드 및 재사용을 위해 디스크에 저장
tokenized_ds.save_to_disk(dataset_path)
print(f"\n[SUCCESS] 데이터셋 로컬 저장 완료: {dataset_path}")
print(f"[INFO] 추후 load_from_disk('{dataset_path}')를 통해 즉시 불러올 수 있습니다.")


# 불러올 데이터의 개수(파일명 숫자)를 입력하세요 (예: 300) : 500
# [INFO] 'movie_500.csv' 로드 완료! (총 데이터: 500개)

# [INFO] 데이터 샘플 (상위 5개):
#                 content  label
# 0        스토리가 너무 지루했어요!      0
# 1    분위기가 시간 가는 줄 몰랐어요~      1
# 2  이 영화가 추천하고 싶지 않아요...      0
# 3           스토리가 명작이네요!      1
# 4        연출가 기대 이상이었어요!      1
# Map: 100%|███████████████████████████████████████████| 400/400 [00:00<00:00, 2730.99 examples/s]
# Map: 100%|███████████████████████████████████████████| 100/100 [00:00<00:00, 7645.75 examples/s]

# --- 커스텀 데이터셋 준비 완료 ---
# DatasetDict({
#     train: Dataset({
#         features: ['labels', 'input_ids', 'token_type_ids', 'attention_mask'],
#         num_rows: 400
#     })
#     test: Dataset({
#         features: ['labels', 'input_ids', 'token_type_ids', 'attention_mask'],
#         num_rows: 100
#     })
# })

# 첫 번째 학습 데이터 샘플 (텐서 구조 확인):
#  {'labels': tensor(0), 'input_ids': tensor([   101,   8881,  89523,  11287,   8932,  14423,   9638,  35506, 119147,
#          12965,  48549,    132,    132,    102,      0,      0,      0,      0,
#              0,      0,      0,      0,      0,      0,      0,      0,      0,
#              0,      0,      0,      0,      0,      0,      0,      0,      0,
#              0,      0,      0,      0,      0,      0,      0,      0,      0,
#              0,      0,      0,      0,      0,      0,      0,      0,      0,
#              0,      0,      0,      0,      0,      0,      0,      0,      0,
#              0]), 'token_type_ids': tensor([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 'attention_mask': tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])}
# Saving the dataset (1/1 shards): 100%|██████████████| 400/400 [00:00<00:00, 88333.68 examples/s]
# Saving the dataset (1/1 shards): 100%|██████████████| 100/100 [00:00<00:00, 22958.59 examples/s]

# [SUCCESS] 데이터셋 로컬 저장 완료: c:\workAI\work\HuggingFace\2.tokenizer\data\my_custom_dataset_500
# [INFO] 추후 load_from_disk('c:\workAI\work\HuggingFace\2.tokenizer\data\my_custom_dataset_500')를 통해 즉시 불러올 수 있습니다.

