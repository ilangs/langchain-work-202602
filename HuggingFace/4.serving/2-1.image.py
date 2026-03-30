# 2.image.py (허깅페이스(웹앱(streamlit), gradio 배포, 미니프로젝트))

import gradio as gr
import numpy as np

#1.모델 역할을 함수 정의 (이미지 처리 함수)
def classify_iamge(img):
    avg_brightness = np.mean(img) # 0~255
    
    if avg_brightness > 127 :
        return {"밝은 이미지":1.0, "어두운 이미지":0.0}
    else:
        return {"밝은 이미지":0.0, "어두운 이미지":1.0}

#2.Gradio 인터페이스 설정
demo = gr.Interface(       # 화면 디자인 및 관련 함수 호출 설정
    fn = classify_iamge,                    # 실행할 함수명
    inputs = gr.Image(),                    # 입력창 (이미지 업로드/드래그)
    outputs = gr.Label(num_top_classes=2),  # 결과창 (분류라벨 수치가 표시)
    title = "이미지 분석기",                  # 웹페이지 제목
    )  

#3.실행
if __name__ == "__main__":
    demo.launch()