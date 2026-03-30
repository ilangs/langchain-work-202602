# 1.pipeliens.py
# pipeline => 데이터 수집->모델훈련->성능테스트->결과까지 한꺼번에 처리
from transformers import pipeline

# 자연어 분석(감정분석)->sentiment-analysis=>텍스트의 감정분석(task)
classifier = pipeline("sentiment-analysis",
                      # distilbert-base-uncased : DistilBERT 기반의 경량화된 BERT 모델
                      # finetuned-sst-2-english : SST-2 감정 분석 데이터셋으로 추가 학습된 모델
                      model="distilbert-base-uncased-finetuned-sst-2-english"
                      )

# 분석할 문장들을 리스트로 준비
sentences = [
    "I love using Hugging Face transformers!",  # 긍정적인 문장 예시
    "That is wonderful magic!"                  # 또 다른 긍정적인 문장 예시

    # --- 긍정적인 문장 (Positive) ---
    "The new API latency is incredibly fast and highly reliable.",                  # 긍정 3
    "I am so impressed with how easy it is to deploy this model.",                  # 긍정 4
    "LangChain has beautifully streamlined our team's RAG workflow.",               # 긍정 5
    "This open-source framework is a fantastic alternative to proprietary models.", # 긍정 6
    
    # --- 부정적인 문장 (Negative) ---
    "I am deeply disappointed with the recent API price increase.",                     # 부정 1
    "The documentation is confusing and lacks proper examples.",                        # 부정 2
    "This local model is painfully slow and frequently crashes on my machine.",         # 부정 3
    "It's absolutely frustrating when ChromaDB throws unexplained connection errors.",  # 부정 4
    "I hate how complicated and unstable the new update made our pipeline.",            # 부정 5
    "The generated response was completely inaccurate and a waste of compute."          # 부정 6
]

# 감정분석
results = classifier(sentences) # 모델에게 긍정 or 부정 질문 => 신뢰도 비율?

# 각 문장과 결과를 함께 출력하기 위해 반복문 사용
for sentence, result in zip(sentences, results):
    print(f"문장: {sentence}")  # 원본 문장 출력
    #결과물->감성(label: POSITIVE/NEGATIVE 등)과 신뢰도(score)를 소수점 4자리까지 출력
    print(f"감성: {result['label']}, 신뢰도: {result['score']:.4f}")  
    
'''
문장: I love using Hugging Face transformers!
감성: POSITIVE, 신뢰도: 0.9971
문장: That is wonderful magic!I love using Hugging Face transformers!
감성: POSITIVE, 신뢰도: 0.9999
문장: That is wonderful magic!
감성: POSITIVE, 신뢰도: 0.9999
문장: The new API latency is incredibly fast and highly reliable.
감성: POSITIVE, 신뢰도: 0.9997
문장: I am so impressed with how easy it is to deploy this model.
감성: POSITIVE, 신뢰도: 0.9988
문장: LangChain has beautifully streamlined our team's RAG workflow.
감성: POSITIVE, 신뢰도: 0.9998
문장: This open-source framework is a fantastic alternative to proprietary models.
감성: POSITIVE, 신뢰도: 0.9998
문장: I am deeply disappointed with the recent API price increase.
감성: NEGATIVE, 신뢰도: 0.9997
문장: The documentation is confusing and lacks proper examples.
감성: NEGATIVE, 신뢰도: 0.9998
문장: This local model is painfully slow and frequently crashes on my machine.
감성: NEGATIVE, 신뢰도: 0.9997
문장: It's absolutely frustrating when ChromaDB throws unexplained connection errors.
감성: NEGATIVE, 신뢰도: 0.9992
문장: I hate how complicated and unstable the new update made our pipeline.
감성: NEGATIVE, 신뢰도: 0.9997
문장: The generated response was completely inaccurate and a waste of compute.
감성: NEGATIVE, 신뢰도: 0.9998
'''