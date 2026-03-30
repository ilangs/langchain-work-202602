# 7.fullpipeline.py파일 작성

import pandas as pd                         # 엑셀/CSV 데이터를 다루는 판다스 임포트
from datasets import Dataset, DatasetDict   # 허깅페이스 데이터셋 변환 도구 임포트
from transformers import AutoTokenizer      # 허깅페이스 자동 토크나이저 로더 임포트
import os                                   # 파일 경로 제어 모듈

# 1. 가상의 CSV 데이터 생성 (실무에서는 pd.read_csv("my_data.csv")로 대체하세요)
# 새로 데이터 만들어서 모델로 저장->불러와서 저장->다른 프로젝트에 적용
data = {
    "content": [ # text 필드 대신에 작성 => 최소 300개 ~ 최대 1000개 데이터 학습 필요
        "이 영화 정말 최고예요! 꼭 보세요.",
        "시간 아까워요. 절대 보지 마세요.",
        "그냥 평범한 영화였습니다.",
        "연기력이 대박이네요. 감동적입니다.",
        "스토리가 너무 뻔해서 지루했어요."
    ],
    "label": [1, 0, 1, 1, 0]  # 1: 긍정, 0: 부정
}
df = pd.DataFrame(data)

# 2. 판다스 데이터프레임을 허깅페이스 Dataset 객체로 변환합니다.
# 이 과정을 거쳐야 허깅페이스의 강력한 map 기능을 쓸 수 있습니다.
raw_dataset = Dataset.from_pandas(df)

# 3. 학습(Train)과 검증(Test) 데이터로 분리합니다. (80% 학습, 20% 테스트)
# 실무에서 데이터가 적을 때 아주 유용한 함수입니다.
ds_split = raw_dataset.train_test_split(test_size=0.2)

# 4. 토크나이저 준비 (BERT 다국어 모델 기준)
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

# 5. 전처리 함수 정의
def preprocess_function(examples):
    # 'content' 컬럼을 토큰화하고, 길이를 64로 맞춥니다.
    return tokenizer(examples["content"], truncation=True, padding="max_length", max_length=64)

# 6. 전체 데이터셋에 전처리 적용 (배치 처리로 속도 업!)
tokenized_ds = ds_split.map(preprocess_function, batched=True)

# 7. 모델 학습에 불필요한 'content' 원본 텍스트 컬럼은 제거합니다.
# input_ids, attention_mask, label만 남깁니다.
tokenized_ds = tokenized_ds.remove_columns(["content"])

# 8. 파이토치(PyTorch) 텐서 형식으로 최종 변환
tokenized_ds.set_format("torch")

# 9. 결과 확인
print("--- 커스텀 데이터셋 준비 완료 ---")
print(tokenized_ds)
print("\n첫 번째 학습 데이터 샘플:\n", tokenized_ds["train"][0])

# 10. (옵션) 나중에 다시 쓰기 위해 로컬에 저장해두기
# 현재 파일이 있는 디렉토리 절대경로
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
print('current_dir=>',current_dir) #current_dir=> c:\workAI\work\HuggingFace\2.tokenzier
dataset_path = os.path.join(current_dir, "data", "my_custom_dataset")

tokenized_ds.save_to_disk(dataset_path)

'''
--- 커스텀 데이터셋 준비 완료 ---
DatasetDict({
    train: Dataset({
        features: ['label', 'input_ids', 'token_type_ids', 'attention_mask'],
        num_rows: 4
    })
    test: Dataset({
        features: ['label', 'input_ids', 'token_type_ids', 'attention_mask'],
        num_rows: 1
    })
})

첫 번째 학습 데이터 샘플:
 {'label': tensor(0), 'input_ids': tensor([   101,   9477,  26444,  44130,   9004,  32537,   9394,  70146,   9706,
         35866, 119424,  12965,  48549,    119,    102,      0,      0,      0,
             0,      0,      0,      0,      0,      0,      0,      0,      0,
             0,      0,      0,      0,      0,      0,      0,      0,      0,
             0,      0,      0,      0,      0,      0,      0,      0,      0,
             0,      0,      0,      0,      0,      0,      0,      0,      0,
             0,      0,      0,      0,      0,      0,      0,      0,      0,
             0]), 'token_type_ids': tensor([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 'attention_mask': tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])}
current_dir=> c:\workAI\work\HuggingFace\2.tokenizer
Saving the dataset (1/1 shards): 100%|████████████████████████| 4/4 [00:00<00:00, 562.16 examples/s] 
Saving the dataset (1/1 shards): 100%|████████████████████████| 1/1 [00:00<00:00, 132.04 examples/s]

'''
