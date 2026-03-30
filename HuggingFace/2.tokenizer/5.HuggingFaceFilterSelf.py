# 5.HuggingFaceFilterSelf.py -> 개별 실습

from datasets import load_dataset

dataset = load_dataset("rotten_tomatoes")


# 1. 데이터셋 나누기 (Train/Test Split) ###################################################
# 학습 데이터(train)만 있을 때, 모델의 성능을 검증하기 위해 데이터를 일정 비율로 나누는 작업입니다.

# 전체 데이터를 8:2 비율로 나눕니다 (test_size=0.2)
split_dataset = dataset["train"].train_test_split(test_size=0.2, seed=42)

print(f"학습용 개수: {len(split_dataset['train'])}")
print(f"검증용 개수: {len(split_dataset['test'])}")


# 2. 새로운 컬럼 추가하기 (map 함수 활용) ####################################################
# 기존 텍스트의 길이를 계산하여 새로운 정보(text_len)를 추가하는 등 데이터를 변환할 때 사용합니다.

# 각 리뷰의 글자 수를 계산하여 'text_len'이라는 새 컬럼을 추가합니다.
def add_length(example):
    example["text_len"] = len(example["text"])
    return example

# map 함수를 사용하여 전체 데이터에 적용합니다.
dataset_with_len = dataset["train"].map(add_length)

print(f"첫 번째 문장 길이: {dataset_with_len[0]['text_len']}")


# 3. 불필요한 데이터 제거 및 컬럼 삭제 #######################################################
# 학습에 필요 없는 컬럼을 지우거나, 너무 짧은 리뷰(노이즈)를 제거하여 데이터의 품질을 높입니다.

# 1. 특정 컬럼(예: label) 삭제하기
reduced_dataset = dataset["train"].remove_columns(["label"])

# 2. 리뷰 길이가 20자 미만인 너무 짧은 데이터 필터링 (노이즈 제거)
clean_dataset = dataset["train"].filter(lambda x: len(x["text"]) > 20)

print(f"필터링 전: {len(dataset['train'])} -> 후: {len(clean_dataset)}")


# 4. 데이터 형식 변경 (Pandas 연동) ########################################################
# 데이터 시각화나 복잡한 통계 분석을 위해 허깅페이스 데이터셋을 Pandas DataFrame으로 변환합니다.

import pandas as pd

# 데이터셋을 Pandas 형식으로 변환하여 출력합니다.
dataset.set_format(type="pandas")
df = dataset["train"][:]

# 상위 5개 행 출력 및 통계 확인
print(df.head())
print(df['label'].value_counts()) # 긍정(1)/부정(0) 분포 확인

# 다시 허깅페이스 포맷으로 복구하려면:
dataset.reset_format()


# 5. 데이터 일괄 수정 (소문자화 및 특수문자 제거) ############################################
# 전처리 과정에서 텍스트를 정규화하여 모델이 단어를 더 잘 인식하게 만듭니다.

import re

def clean_text(example):
    # 소문자로 변환하고 특수문자를 제거하는 정규식 적용
    text = example["text"].lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return {"text": text}

# batched=True를 사용하면 여러 데이터를 한꺼번에 빠르게 처리합니다.
preprocessed_dataset = dataset["train"].map(clean_text, batched=False)

print(f"전처리 후 문장: {preprocessed_dataset[0]['text']}")