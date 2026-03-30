# 4.HuggingFaceRead.py

from datasets import load_dataset

# 1. 허깅페이스 허브에서 'rotten_tomatoes'(영화 리뷰) 데이터셋을 내려받습니다.
dataset = load_dataset("rotten_tomatoes")

# 2. 데이터셋의 구조(train, validation, test)를 확인합니다.
# print("데이터셋 구조:", dataset) train,validation,test
# 특정 세트 접근해서 활용
train_data = dataset["train"]

# 3. 학습용 데이터(train)의 첫 번째 샘플을 확인합니다. (지도학습 기존데이터+라벨링 데이터)
# 'text'와 'label'(0:부정, 1:긍정)로 구성되어 있습니다.
print(f"문장:{train_data[0]['text']}")
print(f"정답:{train_data[0]['label']}")

# 4. 전체 개수 확인하기
print(f"학습 데이터 개수: {len(train_data)}")

'''
문장:the rock is destined to be the 21st century's new " conan " and that he's going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .
정답:1
학습 데이터 개수: 8530

"더 락(드웨인 존슨)은 21세기의 새로운 '코난'이 될 운명이며, 아놀드 슈왈제네거, 장클로드 반담, 혹은 스티븐 시걸보다 
훨씬 더 큰 파장을 일으킬 것이다."
'''
