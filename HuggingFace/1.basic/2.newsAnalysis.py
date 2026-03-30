# 2.newsAnalysis.py
# pipeline => 데이터 수집->모델훈련->성능테스트->결과까지 한꺼번에 처리
from transformers import pipeline

# 자연어 분석(감정분석)->sentiment-analysis=>텍스트의 감정분석(task)
# classifier = pipeline("sentiment-analysis",
#                       model="snunlp/KR-FinBert-SC",
#                       framework="pt")
'''
뉴스 기사: {'오늘 주식시장은 투자자들의 불안으로 인해 큰 폭으로 하락했습니다.'}
감정 분석 결과: neutral
확률 점수: 0.6733
'''  

classifier = pipeline("sentiment-analysis",
                      model="beomi-kcbert-base",
                      framework="pt"
                    )

news_text = "오늘 주식시장은 투자자들의 불안으로 인해 큰 폭으로 하락했습니다." 

result = classifier(news_text) # 모델에게 긍정 or 부정 질문 => 신뢰도 비율?

print("뉴스 기사:", {news_text})  # 원본 문장 출력
print("감정 분석 결과:", result[0]['label'])     # 긍정/부정 라벨 출력
print("확률 점수:", round(result[0]['score'],4)) # 신뢰도 점수 출력

  