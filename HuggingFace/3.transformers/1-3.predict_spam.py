# s3.predict_spam.py: 실시간 판별 추론기 (웹 서비스나 챗봇에 연동할 때 사용하는 가벼운 스크립트)
# 학습이 완료된 폴더(모델+토크나이저)만 불러와서 즉시 새로운 문장의 스팸 여부를 판별(대화형)

import os
import sys
from transformers import pipeline

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_count = input("불러올 모델 숫자 입력 (예: 500) : ")
    # 위 2번 파일에서 저장한 이름과 맞춥니다.
    model_path = os.path.join(base_dir, "data", f"my_spam_model_{data_count}_klue")
    
    print("\n[INFO] 로딩 중...")
    spam_classifier = pipeline("text-classification", model=model_path, tokenizer=model_path)
    print("[SUCCESS] 완료! 문자를 입력해보세요.\n")
    
    while True:
        user_msg = input("문자 입력 (종료 'q') : ")
        if user_msg.lower() == 'q': break
        if not user_msg: continue
            
        result = spam_classifier(user_msg)[0]
        
        # 모델이 SPAM, HAM 으로 대답하도록 세팅해두었음
        if result["label"] == "SPAM":
            print(f"👉 결과: 🚨 스팸(Spam) 의심! ({result['score']*100:.1f}%)\n")
        else:
            print(f"👉 결과: ✅ 정상(Ham) 문자 ({result['score']*100:.1f}%)\n")

if __name__ == "__main__":
    main()

    # 테스트용 문구
    # 안녕하세요 팀장님, 내일 점심 식사 가능하신가요?
    # 축하합니다! 1억 원 경품에 당첨되셨습니다. 지금 클릭!
    # 광고) 최저 금리 대출 상품 안내 드립니다.