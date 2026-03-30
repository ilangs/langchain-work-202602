# 10.modelTrainSelf.py

import os
import sys
from datasets import load_from_disk
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

# -------------------------------------------------------------------
# 0. 스크립트 실행 위치 기준 절대 경로 지정 (Windows 경로 오류 방지)
# -------------------------------------------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------------------
# 1. 전처리된 데이터셋 불러오기
# -------------------------------------------------------------------
try:
    data_count = input("학습에 사용할 데이터 개수(이전 파이프라인에서 입력한 숫자)를 입력하세요 (예: 300) : ")
except Exception as e:
    print(f"[ERROR] 입력 처리 중 오류 발생: {e}")
    sys.exit(1)

# 이전 파이프라인에서 저장한 동적 데이터셋 폴더 경로 구성
dataset_folder_name = f"my_custom_dataset_{data_count}"
dataset_path = os.path.join(base_dir, "data", dataset_folder_name)

if not os.path.exists(dataset_path):
    print(f"[ERROR] '{dataset_path}' 폴더를 찾을 수 없습니다.")
    print("[ERROR] 7.fullpipeline.py 스크립트를 먼저 실행하여 데이터셋을 생성해주세요.")
    sys.exit(1)

print(f"[INFO] '{dataset_folder_name}' 데이터셋을 로드합니다...")
tokenized_ds = load_from_disk(dataset_path)

# -------------------------------------------------------------------
# 2. 분류 모델 로드 (BERT 다국어 모델)
# -------------------------------------------------------------------
model_name = "bert-base-multilingual-cased"
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# -------------------------------------------------------------------
# 3. 학습 환경 설정 (동적 경로 적용)
# -------------------------------------------------------------------
# 데이터 개수에 따라 결과(체크포인트)와 로그 저장 폴더명 분리
output_dir = os.path.join(base_dir, "data", "results", f"run_{data_count}")
logging_dir = os.path.join(base_dir, "data", "logs", f"run_{data_count}")

training_args = TrainingArguments(
    output_dir=output_dir,           # 결과 및 체크포인트 저장 경로
    learning_rate=2e-5,              # 학습률
    per_device_train_batch_size=8,   # 배치 사이즈
    num_train_epochs=3,              # 에포크
    weight_decay=0.01,               # 가중치 감쇠
    logging_dir=logging_dir,         # 로그 경로
    remove_unused_columns=False      # 안전을 위한 설정 유지
)

# -------------------------------------------------------------------
# 4. 트레이너(Trainer) 정의
# -------------------------------------------------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_ds["train"],
    eval_dataset=tokenized_ds["test"],
)

# -------------------------------------------------------------------
# 5. 학습 시작
# -------------------------------------------------------------------
print(f"--- 최저 사양 호환 모드로 학습을 시작합니다 (데이터: {data_count}개) ---")
try:
    trainer.train()
except TypeError as e:
    print("\n[치명적 오류] 현재 설치된 transformers와 accelerate 버전이 서로 호환되지 않습니다.")
    print("해결책: pip install accelerate==0.34.1 를 입력해 버전을 맞춰주세요.")
    raise e

# -------------------------------------------------------------------
# 6. 최종 모델 저장 (동적 폴더명 적용)
# -------------------------------------------------------------------
# 데이터 개수에 맞춘 최종 모델 저장 폴더 (예: my_movie_model_300)
final_model_dir = os.path.join(base_dir, "data", f"my_movie_model_{data_count}")

model.save_pretrained(final_model_dir)

# 토크나이저도 나중에 추론(Inference)을 위해 동일한 폴더에 함께 저장하는 것을 권장합니다.
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(final_model_dir)

print(f"\n[SUCCESS] 학습 완료! 최종 모델과 토크나이저가 '{final_model_dir}' 폴더에 저장되었습니다.")


# 학습에 사용할 데이터 개수(이전 파이프라인에서 입력한 숫자)를 입력하세요 (예: 300) : 500
# [INFO] 'my_custom_dataset_500' 데이터셋을 로드합니다...

# --- 최저 사양 호환 모드로 학습을 시작합니다 (데이터: 500개) ---

# {'train_runtime': 189.5343, 'train_samples_per_second': 6.331, 'train_steps_per_second': 0.791, 'train_loss': 0.1792400868733724, 'epoch': 3.0}
# 100%|█████████████████████████████████████████████████████████| 150/150 [03:09<00:00,  1.26s/it] 

# [SUCCESS] 학습 완료! 최종 모델과 토크나이저가 'c:\workAI\work\HuggingFace\2.tokenizer\data\my_movie_model_500' 폴더에 저장되었습니다.

