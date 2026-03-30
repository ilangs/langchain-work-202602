# 2-2.googleVitModel.py

import gradio as gr  # Gradio: 웹 기반 UI를 쉽게 만들기 위한 라이브러리
import torch  # PyTorch: 딥러닝 모델 실행 및 텐서 연산 처리
from PIL import Image  # PIL: 이미지 파일을 처리하기 위한 라이브러리 (numpy ↔ 이미지 변환)

#  ViT 모델 관련 클래스 import
from transformers import ViTImageProcessor, ViTForImageClassification
# ViTImageProcessor: 이미지 전처리 (리사이즈, 정규화 등)
# ViTForImageClassification: ViT 기반 이미지 분류 모델

# 사용할 사전 학습 모델 이름 (Vision Transformer)
model_name = "google/vit-base-patch16-224"

# 이미지 전처리기 로드 (자동으로 모델에 맞는 전처리 적용)
processor = ViTImageProcessor.from_pretrained(model_name)


# 이미지 분류 모델 로드 (사전 학습된 가중치 자동 다운로드)
model = ViTForImageClassification.from_pretrained(model_name)

# 이미지 분류 함수 정의 (Gradio에서 호출됨)
def classify_image(img):

    # 입력 이미지가 torch.Tensor 타입이면 numpy 배열로 변환
    if isinstance(img, torch.Tensor):
        img = img.numpy()

    # numpy 배열을 PIL 이미지 객체로 변환 (모델 입력 형식 맞추기)
    img = Image.fromarray(img)

    # 모델 입력을 위한 전처리 수행
    inputs = processor(images=img, return_tensors="pt")
    # 내부적으로:
    # - 이미지 크기 224x224로 변환
    # - 정규화 수행
    # - PyTorch 텐서로 변환

    # 모델 예측 수행 (추론 모드)
    with torch.no_grad():  # gradient 계산 비활성화 (속도 + 메모리 최적화)
        outputs = model(**inputs)  # 모델에 입력 데이터 전달
        logits = outputs.logits  # 모델의 원시 출력값 (확률이 아님)

    # Softmax 함수로 logits → 확률로 변환
    probs = torch.nn.functional.softmax(logits, dim=-1)[0]
    # dim=-1: 클래스 차원 기준으로 확률 계산

    # 확률이 높은 상위 3개 클래스 추출
    top3_prob, top3_indices = torch.topk(probs, 3)

    # 결과를 저장할 딕셔너리 생성
    results = {}

    #상위 3개 결과 반복 처리
    for i in range(3):
        # 클래스 인덱스를 실제 라벨 이름으로 변환
        label = model.config.id2label[top3_indices[i].item()]

        # 라벨과 해당 확률을 딕셔너리에 저장
        results[label] = float(top3_prob[i])

    # 최종 결과 반환 (Gradio Label에 출력됨)
    return results

# Gradio 인터페이스 생성
demo = gr.Interface(
    fn=classify_image,  # 이미지 입력 시 실행할 함수
    inputs=gr.Image(
        type="numpy",  # 입력 이미지를 numpy 배열로 전달
        sources=["upload"]  # 업로드 방식만 허용
    ),

    outputs=gr.Label(num_top_classes=3),  # 상위 3개 클래스 결과를 시각적으로 출력
    
    title="ViT 이미지 분류기",  # 웹 페이지 제목

    description="ViT 모델을 사용한 이미지 분류"  # 서비스 설명
)

# 프로그램 실행 진입점
if __name__ == "__main__":  # 현재 파일을 직접 실행할 때만 동작
    demo.launch(inbrowser=True)      # Gradio 서버 실행 + 웹 브라우저 자동 실행
