# 1.text.py (허깅페이스(웹앱(streamlit), gradio 배포, 미니프로젝트))

import gradio as gr

#1.모델 역할을 함수 정의
def predict_sentiment(text):
    if "좋아" in text or "행복해" in text:
        return "긍정적인 메세지 입니다."
    elif "슬프다" in text or "화난다" in text:
        return "조금 우울해 보입니다. 힘내세요."
    else:
        return "평범한 메세지입니다."

#2.Gradio 인터페이스 설정
demo = gr.Interface(    # 화면 디자인 및 관련 함수 호출 설정
    fn = predict_sentiment,                                       # 실행할 함수명
    inputs = gr.Textbox(placeholder="여기에 문장을 입력하세요..."),   # 입력창
    outputs = "text",                                             # 결과창 (텍스트)
    title = "텍스트 감성 분석기",                                    # 웹페이지 제목
    description = "입력한 문장의 분위기를 AI가 분석 합니다."            # 설명
    )  

#3.실행
if __name__ == "__main__":
    demo.launch()