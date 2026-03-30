# 6.pytorch.py파일 작성

from transformers import AutoTokenizer  # 허깅페이스 자동 토크나이저 로더 임포트
from datasets import load_dataset       # 데이터셋 로드 함수 임포트
import torch                            # 파이토치 라이브러리 임포트

# --- [준비 단계: 데이터셋 로드] ---
# 실습을 위해 영화 비평 데이터셋을 불러옵니다. (위의 코드들이 동작하기 위한 전제 조건)
dataset = load_dataset("rotten_tomatoes")

# --- [1. 토크나이저 설정 및 기초 테스트] ---
# 사전 학습된 BERT 다국어 모델의 토크나이저를 불러옵니다.
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

# 길이가 다른 두 개의 샘플 문장을 준비합니다.
sentences = ["반갑습니다.", "허깅페이스 데이터셋 전처리를 배우는 중입니다."]

# 텍스트를 숫자로 변환합니다. 
# padding="max_length": 짧은 문장은 0(PAD)으로 채워 길이를 맞춤
# truncation=True: max_length(10)보다 긴 문장은 자름
encoded = tokenizer(sentences, padding="max_length", max_length=10, truncation=True)

# 인코딩 결과(정수 ID 리스트)를 출력합니다.
print("기초 테스트 인코딩 ID:", encoded["input_ids"]) # 숫자화 확인
'''
기초 테스트 인코딩 ID: [
    [101, 9321, 118610, 119081, 48345, 119, 102, 0, 0, 0],
    [101, 100, 9083, 85297, 119048, 9665, 60469, 27852, 84703, 102]
    ] -> 문자열 => 길이 맞추어서 자동으로 토큰화 -> 숫자로 만들어 준다.
'''
# --- [2. 전체 데이터셋 일괄 전처리 함수] ---
# 데이터셋의 각 샘플(examples)을 받아서 토크나이징을 수행하는 함수를 정의합니다.
def tokenize_fn(examples):  # 반복처리 -> FOR문 역할로 함수를 이용할 수 있다.
    # 'text' 컬럼의 데이터를 가져와 128 길이에 맞춰 변환합니다.
    # return되는 값에는 input_ids, attention_mask 등이 포함됩니다.
    return tokenizer(examples["text"], padding="max_length", max_length=128, truncation=True)

# map 함수를 사용하여 전체 데이터셋에 tokenize_fn을 적용합니다.
# batched=True: 데이터를 하나씩 처리하지 않고 묶음으로 처리하여 속도를 대폭 향상시킵니다.
tokenized_dataset = dataset.map(tokenize_fn, batched=True)

# 전처리가 완료된 후 데이터셋에 어떤 컬럼들이 새로 생겼는지 확인합니다.
print("추가된 컬럼:", tokenized_dataset["train"].column_names) # 컬럼명 확인 가능
'''
추가된 컬럼: ['text', 'label', 'input_ids', 'token_type_ids', 'attention_mask']
'''

# --- [3. 모델 학습을 위한 포맷 변환] ---
# 학습에 불필요한 원본 텍스트 등은 제외하고, 모델 입력에 필요한 컬럼만 추출하여 
# 파이토치(PyTorch) 텐서(Tensor) 형식으로 변환합니다.
tokenized_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

# 변환이 잘 되었는지 첫 번째 데이터를 꺼내 확인합니다.
final_sample = tokenized_dataset["train"][0]

# input_ids의 데이터 타입을 출력하여 'torch.Tensor'가 나오는지 확인합니다.
print("최종 데이터 타입 확인:", type(final_sample["input_ids"]))
# 실제 텐서 데이터의 형태(Shape)도 확인해봅니다. (길이가 128인지 확인)
print("첫 번째 샘플 텐서 크기:", final_sample["input_ids"].shape)
'''
최종 데이터 타입 확인: <class 'torch.Tensor'>
첫 번째 샘플 텐서 크기: torch.Size([128])
'''
