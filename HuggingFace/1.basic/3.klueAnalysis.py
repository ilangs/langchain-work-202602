# 3.klueAnalysis.py파일 작성
# pipeline => 데이터 수집->모델훈련->성능테스트->결과까지 한꺼번에 처리
from transformers import pipeline

# text-classification 텍스트 분류
# klue/robert-base => 한국어 자연어 처리에 특회된 모델 => 0.5~0.7 사이 정상
classifier = pipeline("text-classification",                     # task:텍스트 분류
                      model="monologg/kobigbird-bert-base",      # 사용모델:klue/robert-base
                      tokenizer="monologg/kobigbird-bert-base",  # 토크나이저(단어쪼개기(문장))->모델명과 동일
                      framework="pt"                             # pytorch 사용 옵션
                      )
# 토크나이저: 생략 권장(내부적으로 자동, 동일모델 호출), 다른 모델 사용시 토큰분해방식이 달라져 결괴왜곡

'''
"klue/roberta-base"
뉴스 기사: {'오늘 날씨가 너무 좋아서 기분이 상쾌합니다.'}
감정 분석 결과: LABEL_0
확률 점수: 0.5488

"klue/roberta-large"
뉴스 기사: {'오늘 날씨가 너무 좋아서 기분이 상쾌합니다.'}
감정 분석 결과: LABEL_0
확률 점수: 0.6245

"snunlp/KR-FinBert-SC"
뉴스 기사: {'오늘 날씨가 너무 좋아서 기분이 상쾌합니다.'}
감정 분석 결과: neutral
확률 점수: 0.9986

"monologg/kobigbird-bert-base"
뉴스 기사: {'오늘 날씨가 너무 좋아서 기분이 상쾌합니다.'}
감정 분석 결과: LABEL_0
확률 점수: 0.5134
'''

news_text = "오늘 날씨가 너무 좋아서 기분이 상쾌합니다."

result = classifier(news_text) # 모델에게 긍정 or 부정 질문 => 신뢰도 비율?

print("뉴스 기사:", {news_text})                   # 원본 문장 출력
print("감정 분석 결과:", result[0]['label'])       # 긍정/부정 라벨 출력
print("확률 점수:", round(result[0]['score'],4))   # 신뢰도 점수 출력


# 1.snunlp/KR-FinBert-SC (경제/금융 뉴스 1순위)
# 특징: 서울대 NLP 랩에서 한국어 경제 뉴스, 기업 공시 데이터로 학습시킨 모델입니다. 
# "하락", "어닝 쇼크", "불안" 등 금융권 특화 어휘의 문맥을 완벽히 이해합니다.

# 2.klue/roberta-large 기반 Fine-tuned 모델 (일반 뉴스 1순위)
# 특징: 파라미터 수가 커서 문맥 이해도가 가장 높습니다. 허브에서 klue/roberta-large를 
# 기반으로 NLI나 감정분석으로 파인튜닝된 파생 모델을 찾아 쓰시면 일반 사회/정치 뉴스 분류에 탁월합니다.

# 3.monologg/kobigbird-bert-base (장문 뉴스 특화)
# 특징: BERT 모델들은 구조적으로 512 토큰(약 300~400단어)까지만 읽을 수 있어, 긴 뉴스는 뒷부분이 잘립니다.
# BigBird 아키텍처는 최대 4096 토큰까지 한 번에 읽을 수 있어, 기사 원문 전체를 넣고 분석할 때 유일한 대안입니다.
