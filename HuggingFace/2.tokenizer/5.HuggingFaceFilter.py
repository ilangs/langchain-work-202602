#5.HuggingFaceFilter.py 파일 작성

from datasets import load_dataset

# 1. 허깅페이스 허브에서 'rotten_tomatoes'(영화 리뷰) 데이터셋을 내려받습니다.
dataset = load_dataset("rotten_tomatoes")

# 2. 특정 세트 접근하기 (시트 선택)
train_data = dataset["train"]

# 3. 첫 번째 문장과 정답 확인하기
print(f"문장: {train_data[0]['text']}")
print(f"정답: {train_data[0]['label']}")#1 =>감정적으로 긍정의 부분이기에 1이 부여됨.

# 4. 전체 개수 확인하기
print(f"학습 데이터 개수: {len(train_data)}")

# 5. 리뷰 내용 중에 'perfect'라는 단어가 포함된 긍정적인 리뷰만 골라냅니다.
# filter 함수는 조건이 True인 데이터만 남깁니다.
filtered_data = dataset["train"].filter(lambda x: "perfect" in x["text"].lower())

# 6. 필터링된 데이터의 개수를 확인합니다.
print(f"'perfect'가 포함된 리뷰 개수: {len(filtered_data)}") # perfect'가 포함된 리뷰 개수:76

# 7. 데이터를 무작위로 섞습니다(학습 시 편향을 막기 위해 필수!)
#seed=42 seed=1,2 써도 된다 (일정한 값이 나오게 하기 위해서)
shuffled_dataset = dataset["train"].shuffle(seed=42) 

# 8. 텍스트 길이 순서대로 정렬합니다.
sorted_dataset = dataset["train"].sort("text")

# 9. 가장 짧은 텍스트 확인
print("가장 짧은 리뷰:", sorted_dataset[0]["text"]) # 가장 짧은 리뷰: " 13 conversations " holds its goodwill close , but is relatively slow to come to the point .



