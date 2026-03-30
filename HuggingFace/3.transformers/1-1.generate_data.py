# s1.generate_data.py: 데이터 수집 및 CSV 생성 (언제든 데이터만 따로 늘리기 위해 분리)
# 언제든 필요한 만큼 가상의 스팸/정상 데이터를 생성하여 data 폴더에 CSV 형식으로 저장

import os
import sys
import random
import itertools
import pandas as pd

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("--- [1단계] 스팸 판별 학습용 데이터 생성 ---")
    try:
        user_input = input("생성할 데이터 총 개수를 입력하세요 (예: 300, 500, 1000) : ")
        total_count = int(user_input)
        if total_count <= 0:
            raise ValueError
        if total_count % 2 != 0:
            total_count += 1
            print(f"[WARN] 50:50 비율을 위해 개수를 {total_count}개로 조정합니다.")
    except ValueError:
        print("[ERROR] 유효한 양의 정수를 입력해주세요.")
        sys.exit(1)
        
    half_n = total_count // 2
    
    # ---------------------------------------------------------
    # [수정됨] 단어 풀 확장 (10 x 10 x 10 = 1,000 조합 가능)
    # ---------------------------------------------------------
    # 스팸 문장 생성용 단어 풀
    spam_words1 = ["(광고)", "당첨!", "대출", "주식", "특가", "무료", "VIP", "긴급", "마지막 기회", "초특가"]
    spam_words2 = ["최저 금리", "무료 쿠폰", "급등 종목", "최대 80% 할인", "사은품 증정", "수익 보장", "무보증 대출", "포인트 지급", "전액 지원", "특별 이벤트"]
    spam_words3 = ["아래 링크를 클릭하세요.", "지금 바로 신청하세요.", "상담 받아보세요.", "다운로드 하세요.", "연락 바랍니다.", "확인해 보세요.", "절대 놓치지 마세요.", "서둘러 참여하세요.", "고객센터로 문의하세요.", "앱에서 확인하세요."]
    
    # 정상 문장 생성용 단어 풀
    ham_words1 = ["오늘", "내일", "이번 주", "팀장님", "고객님", "대리님", "프로젝트", "회의", "점심", "다음 주"]
    ham_words2 = ["회의 시간", "요청하신 자료", "카드 명세서", "택배 배송", "결제 내역", "업무 보고서", "계약서 초안", "휴가 신청서", "미팅 준비", "일정 변경"]
    ham_words3 = ["확인 부탁드립니다.", "송부해 드립니다.", "도착 예정입니다.", "검토 바랍니다.", "언제 시간 되시나요?", "수정 완료했습니다.", "참고 부탁드립니다.", "다시 연락드리겠습니다.", "미리 감사드립니다.", "공지사항 확인 바랍니다."]
    # ---------------------------------------------------------
    
    # 모든 가능한 조합 생성 (데카르트 곱)
    spam_comb = list(itertools.product(spam_words1, spam_words2, spam_words3))
    ham_comb = list(itertools.product(ham_words1, ham_words2, ham_words3))
    
    if half_n > len(spam_comb):
        print(f"[ERROR] 중복 없이 생성 가능한 최대 개수는 {len(spam_comb)*2}개입니다.")
        sys.exit(1)
        
    spam_sentences = [f"{w1} {w2} {w3}" for w1, w2, w3 in spam_comb]
    ham_sentences = [f"{w1} {w2} {w3}" for w1, w2, w3 in ham_comb]
    
    # 중복 없는 무작위 추출
    content = random.sample(spam_sentences, half_n) + random.sample(ham_sentences, half_n)
    labels = [1] * half_n + [0] * half_n  # 1: 스팸, 0: 정상
    
    # 데이터프레임 생성 및 섞기
    df = pd.DataFrame({"text": content, "label": labels})
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # 저장 경로 설정
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, f"spam_{total_count}.csv")
    
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"\n[SUCCESS] 총 {len(df)}개의 데이터가 '{csv_path}'에 저장되었습니다.")
    print("-> 다음 단계인 '2.train_model.py'를 실행해주세요.")

if __name__ == "__main__":
    main()
