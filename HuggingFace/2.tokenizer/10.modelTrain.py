# 10.modelTrain.py파일 작성

from datasets import load_from_disk
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TrainingArguments, Trainer
import os, sys

# 1. 전처리된 데이터셋 불러오기
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_dir, "data", "my_custom_dataset")

if not os.path.exists(dataset_path):
    print(f"오류: {dataset_path} 폴더가 없습니다.")
    exit()

tokenized_ds = load_from_disk(dataset_path)

# 2. 분류 모델 로드
model_name = "bert-base-multilingual-cased"
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
# 추후 예측(Inference) 시 텍스트를 변환하기 위해 토크나이저도 함께 불러옵니다.
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 3. 학습 환경 설정 
output_dir = os.path.join(current_dir, "data", "results", "run_class")
logging_dir = os.path.join(current_dir, "data", "logs", "run_class")

training_args = TrainingArguments(
    output_dir=output_dir,          # 결과 저장 경로
    learning_rate=2e-5,              # 학습률: 모델이 학습할 때 가중치를 얼마나 세밀하게 조정헐지ㅏ 결정
    per_device_train_batch_size=8,   # 배치 사이즈: 한번의 학습 단계에서 모델에게 주입할 문장의 갯수
    num_train_epochs=3,              # 에포크: 전체 300개의 데이터를 총 3번 반복 학습시키겠다는 의미
    weight_decay=0.01,               # 가중치 감쇠: 모델이 특정 데이터에만 집착하지 않도록 규제 설정
    logging_dir=logging_dir,            # 로그 경로: 학습과정(오차율)을 기록할 로그파일 경로
    remove_unused_columns=False      # 데이터터셋의 모든 열을 보존하여 학습시 데이터 누락 오류 방지
)

# 4. 트레이너(Trainer) 정의
trainer = Trainer(
    model=model,                         # 매개변수명=전달할값(학습시킬 인공지능 모델을 지정)
    args=training_args,                  # 위에서 설정한 학습환경(=하이퍼파라미터 설정)
    train_dataset=tokenized_ds["train"], # 
    eval_dataset=tokenized_ds["test"],
)

# 5. 학습 시작
print("--- 최저 사양 호환 모드로 학습을 시작합니다 ---")
try:
    trainer.train()
except TypeError as e:
    print("\n[치명적 오류] 현재 설치된 transformers와 accelerate 버전이 호환되지 않습니다.")
    print("코드 수정만으로는 해결이 불가능한 상태입니다.")
    print("해결책: 먼저 pip uninstall accelerate transformers 처리 후,") 
    print("pip install accelerate==0.34.0 transformers==4.45.0 재설치")
    raise e

# 6. 최종 모델 저장
dataset_path2 = os.path.join(current_dir, "data", "my_movie_model")
model.save_pretrained(dataset_path2)
tokenizer.save_pretrained(dataset_path2)

print(f"학습 완료! 모델과 토크나이저가 {dataset_path2} 폴더에 저장되었습니다.")


# --- 최저 사양 호환 모드로 학습을 시작합니다 ---
# 100%|█████████████████████████████████████████████████████████████| 3/3 [00:02<00:00,  1.07it/s]
# 학습 완료! 모델과 토크나이저가 c:\workAI\work\HuggingFace\2.tokenizer\data\my_movie_model 폴더에 저장되었습니다.

