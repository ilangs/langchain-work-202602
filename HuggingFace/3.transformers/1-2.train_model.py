# s2.train_model.py: 데이터 전처리 및 모델 학습 (학습은 GPU 자원을 많이 사용하므로 독립적으로 실행)
# CSV 파일을 읽어와 전처리(토큰화)하고, 인공지능 모델을 학습시킨 뒤 완성된 모델과 토크나이저를 저장
# 기존 모델(bert-base-multilingual-cased) -> 변경 모델(klue/bert-base)

import os
import sys
import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_count = input("학습에 사용할 데이터 개수를 입력하세요 (예: 500) : ")
    csv_path = os.path.join(base_dir, "data", f"spam_{data_count}.csv")
    
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    raw_dataset = Dataset.from_pandas(df)
    ds_split = raw_dataset.train_test_split(test_size=0.2, seed=42)
    
    # 💡 [핵심]  똑똑한 한국어 전용 모델 적용
    model_name = "klue/bert-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    def preprocess_function(examples):
        return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=64)
        
    tokenized_ds = ds_split.map(preprocess_function, batched=True)
    tokenized_ds = tokenized_ds.rename_column("label", "labels")
    tokenized_ds = tokenized_ds.remove_columns(["text"])
    tokenized_ds.set_format("torch")
    
    # 정답 라벨 명확화
    id2label = {0: "HAM", 1: "SPAM"}
    label2id = {"HAM": 0, "SPAM": 1}
    
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=2, id2label=id2label, label2id=label2id
    )
    
    output_dir = os.path.join(base_dir, "results", f"run_{data_count}")
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        learning_rate=3e-5,
        per_device_train_batch_size=16, # GPU가 있으니 배치사이즈를 16으로 늘려 속도업!
        num_train_epochs=4,             # 4번만 봐도 충분히 똑똑해집니다.
        weight_decay=0.01,
        remove_unused_columns=True
    )
    
    trainer = Trainer(model=model, args=training_args, train_dataset=tokenized_ds["train"], eval_dataset=tokenized_ds["test"])
    
    print("\n⚡ GPU를 사용하여 초고속 학습을 시작합니다 ⚡")
    trainer.train()
    
    final_model_dir = os.path.join(base_dir, "data", f"my_spam_model_{data_count}_klue")
    model.save_pretrained(final_model_dir)
    tokenizer.save_pretrained(final_model_dir)
    print(f"\n[SUCCESS] 완료! 모델이 '{final_model_dir}'에 저장되었습니다.")

if __name__ == "__main__":
    main()
