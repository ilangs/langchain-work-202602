# ==============================
# 1. 라이브러리 import
# ==============================

import gradio as gr  # 웹 UI 생성을 위한 Gradio 라이브러리
import torch  # PyTorch (딥러닝 모델 실행 및 텐서 연산)
from PIL import Image  # 이미지 처리 (numpy ↔ PIL 변환)

# ViT 모델 (이미지 분류)
from transformers import ViTImageProcessor, ViTForImageClassification

# BLIP 모델 (이미지 설명 생성)
from transformers import BlipProcessor, BlipForConditionalGeneration

# ==============================
# 2. ViT 모델 로드 (이미지 분류)
# ==============================

# Vision Transformer 모델 이름
model_name = "google/vit-base-patch16-224" 

# 이미지 전처리기 로드 (리사이즈, 정규화 자동 수행)
processor = ViTImageProcessor.from_pretrained(model_name)  

# 이미지 분류 모델 로드 (사전 학습된 가중치 포함)
model = ViTForImageClassification.from_pretrained(model_name)  

# ==============================
# 3. BLIP 모델 로드 (이미지 설명)
# ==============================

# 이미지 → 텍스트 변환을 위한 전처리기
caption_processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"  
)  

# 이미지 설명 생성 모델
caption_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"  
)  

# ==============================
# 4. 이미지 설명 함수 (에러 수정 핵심)
# ==============================

def generate_caption(img):

    # 입력데이터가 PIL 이니지 형식이 아닐 경우 (주로 numpy 배열), PIL 형식 변환
    if not isinstance(img, Image.Image):
        img = Image.fromarray(img)

    # BLIP 입력 전처리 (이미지를 모델 입력용 텐서(pt=PyTorch)로 변환)
    inputs = caption_processor(images=img, return_tensors="pt")

    # 모델 추론 (gradient 미분 계산 비활성화) => 경사하강법(기울기 계산x)
    with torch.no_grad():
        # 모델을 통해 이미지에 대한 텍스트 토큰(숫자 배열) 생성
        out = caption_model.generate(**inputs)

    # 토큰 → 자연어 문장 변환 : 생성된 토큰 번호들을 사람이 읽을수 있는 단어로 변환 (특수토큰 제외)
    caption = caption_processor.decode(out[0], skip_special_tokens=True)

    return caption  # 이미지 설명 반환

# ==============================
# 5. 이미지 분류 + 설명 함수
# ==============================

def classify_image(img):

    #  이미 PIL Image인지 확인 (중복 변환 방지)
    if not isinstance(img, Image.Image):
        img = Image.fromarray(img)

    # ViT 전처리
    inputs = processor(images=img, return_tensors="pt")

    # 모델 예측
    with torch.no_grad():
        outputs = model(**inputs)  # 모델 실행
        logits = outputs.logits  # 원시 출력값

    # Softmax → 확률 변환
    probs = torch.nn.functional.softmax(logits, dim=-1)[0]

    # 상위 3개 결과 추출
    top3_prob, top3_indices = torch.topk(probs, 3)

    results = {}  # 결과 저장용 딕셔너리

    # Top 3 클래스 반복 처리
    for i in range(3):
        label = model.config.id2label[top3_indices[i].item()]  # 라벨 변환
        results[label] = float(top3_prob[i])  # 확률 저장

    # 이미지 설명 생성 (PIL 그대로 전달)
    caption = generate_caption(img)

    # 분류 결과 + 설명 반환
    return results, caption


# ==============================
# 6. Gradio UI 구성
# ==============================

demo = gr.Interface(

    fn=classify_image,  # 실행 함수

    inputs=gr.Image(
        type="numpy",  # numpy 형태로 이미지 입력
        sources=["upload"]  # 업로드 방식
    ),

    outputs=[
        gr.Label(num_top_classes=3),  # 이미지 분류 결과
        gr.Textbox(label="이미지 설명")  # 이미지 설명 출력
    ],

    title="ViT 이미지 분류 + BLIP 이미지 설명",  # 웹 페이지 제목

    description="이미지를 업로드하면 분류 결과와 설명을 함께 제공합니다."  # 서비스 설명
)

# ==============================
# 7. 서버 실행
# ==============================

if __name__ == "__main__":  # 직접 실행 시
    demo.launch(inbrowser=True)    # Gradio 서버 실행 + 브라우저 자동 실행