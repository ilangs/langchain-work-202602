# 8.movieSCVmake.py

import os
import random
import pandas as pd
import itertools
import sys

def generate_reviews(half_n):
    # 긍정 리뷰 생성용 컴포넌트 (10 x 15 x 5 = 750 조합)
    pos_subjects = ["이 영화", "작품", "스토리", "연출", "배우들의 연기", "영상미", "OST", "시나리오", "결말", "분위기"]
    pos_predicates = [
        "정말 최고예요", "완벽합니다", "감동적입니다", "기대 이상이었어요", "여운이 깊게 남네요", 
        "꼭 보세요", "제 인생 영화입니다", "또 보고 싶어요", "대박이네요", "훌륭합니다", 
        "시간 가는 줄 몰랐어요", "명작이네요", "눈물이 났어요", "강력 추천합니다", "압도적이네요"
    ]
    pos_endings = [".", "!", "~", "!!", "..."]
    
    # 부정 리뷰 생성용 컴포넌트 (10 x 15 x 5 = 750 조합)
    neg_subjects = ["이 영화", "전체적인 전개", "스토리", "연출", "배우들의 연기", "결말", "캐릭터 설정", "초반부", "후반부", "CG"]
    neg_predicates = [
        "너무 지루했어요", "시간 아까워요", "올해 최악입니다", "기대 이하였어요", "돈 아깝네요", 
        "절대 보지 마세요", "정말 실망스럽습니다", "엉망이네요", "이해가 전혀 안 가네요", "개연성이 없네요",
        "보다가 중간에 나왔어요", "졸음이 오네요", "추천하고 싶지 않아요", "최악의 경험이었어요", "다시 안 볼 겁니다"
    ]
    neg_endings = [".", "!", "...", "?", ";;"]

    # itertools.product를 사용하여 모든 가능한 조합 생성
    pos_combinations = list(itertools.product(pos_subjects, pos_predicates, pos_endings))
    neg_combinations = list(itertools.product(neg_subjects, neg_predicates, neg_endings))

    # 생성 요청 개수가 최대 조합 가능한 수를 초과하는지 검사
    if half_n > len(pos_combinations):
        print(f"[ERROR] 중복 없이 생성 가능한 최대 개수는 {len(pos_combinations)*2}개입니다.")
        print(f"[ERROR] 입력하신 수량이 너무 많습니다. 프로그램을 종료합니다.")
        sys.exit(1)

    # 문장 형태로 결합
    pos_sentences = [f"{subj}가 {pred}{end}" for subj, pred, end in pos_combinations]
    neg_sentences = [f"{subj}가 {pred}{end}" for subj, pred, end in neg_combinations]

    # 사용자가 요청한 절반(half_n)만큼 각각 중복 없이 무작위 추출 (비복원 추출)
    sampled_pos = random.sample(pos_sentences, half_n)
    sampled_neg = random.sample(neg_sentences, half_n)

    # 데이터프레임 구성을 위해 리스트 병합
    content = sampled_pos + sampled_neg
    # 1: 긍정, 0: 부정
    labels = [1] * half_n + [0] * half_n

    return content, labels

def main():
    # 사용자로부터 데이터 개수 입력받기
    try:
        user_input = input("생성할 데이터 총 개수를 입력하세요 (예: 300) : ")
        total_n = int(user_input)
        
        if total_n <= 0:
            print("[ERROR] 0보다 큰 숫자를 입력해야 합니다.")
            return
            
        # 홀수 입력 시 처리 (50:50 비율을 위해 강제로 짝수 맞춤)
        if total_n % 2 != 0:
            total_n += 1
            print(f"[WARN] 50:50 비율을 맞추기 위해 개수를 {total_n}개로 조정합니다.")
            
    except ValueError:
        print("[ERROR] 유효한 숫자를 입력해주세요.")
        return

    half_n = total_n // 2
    print(f"\n[INFO] 총 {total_n}개(긍정 {half_n}개, 부정 {half_n}개)의 리뷰 데이터 생성을 시작합니다...")
    
    content, labels = generate_reviews(half_n)
    
    # DataFrame 생성
    df = pd.DataFrame({
        "content": content,
        "label": labels
    })
    
    # 데이터 순서 섞기 (긍정/부정이 뭉쳐있지 않도록 random shuffle)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # --- 절대 경로 및 동적 파일명 설정 ---
    # 현재 스크립트 파일 위치 기준 절대 경로 확보
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    # 사용자가 입력한 데이터 수(total_n)를 활용하여 파일명 생성 (예: movie_300.csv)
    file_name = f"movie_{total_n}.csv"
    file_path = os.path.join(data_dir, file_name)
    
    # /data 폴더가 없으면 생성
    os.makedirs(data_dir, exist_ok=True)
    
    # CSV 파일 저장 (인코딩 utf-8-sig로 설정하여 Windows 한글 깨짐 방지)
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    
    print(f"[SUCCESS] 총 {len(df)}개의 데이터가 중복 없이 생성되었습니다.")
    print(f"[SUCCESS] 긍정 리뷰 수: {len(df[df['label'] == 1])}개, 부정 리뷰 수: {len(df[df['label'] == 0])}개")
    print(f"[SUCCESS] 저장 완료: {file_path}\n")

if __name__ == "__main__":
    main()
    

# 생성할 데이터 총 개수를 입력하세요 (예: 300) : 500

# [INFO] 총 500개(긍정 250개, 부정 250개)의 리뷰 데이터 생성을 시작합니다...
# [SUCCESS] 총 500개의 데이터가 중복 없이 생성되었습니다.
# [SUCCESS] 긍정 리뷰 수: 250개, 부정 리뷰 수: 250개
# [SUCCESS] 저장 완료: c:\workAI\work\HuggingFace\2.tokenizer\data\movie_500.csv


