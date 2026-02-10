from callFunction import *
import streamlit as st # 별칭 약어

# API키 불러오기
api_key = st.secrets["OPENAI_API_KEY"] #secrets.toml에서 알아오기

# LLM 초기화
llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0.7)

prompt = PromptTemplate.from_template(" '{topic}' 에 대해서 한 문장으로 설명 해 줘")
output_str = StrOutputParser()
chain = prompt | llm | output_str

#----- streamlit UI 구성 ------

st.set_page_config(page_title="LangChain Chat", page_icon="💬", layout="centered")
# page_title → 브라우저 탭 제목
# page_icon → 브라우저 탭 아이콘
# layout="centered" → 화면 중앙 정렬

st.markdown("### 💬 LangChain + Streamlit 대화형 예제")
# "###" → h3 크기 제목 표시

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []   # 대화 기록 리스트 초기화

def process_input():
    user_text = st.session_state["input_box"].strip()
    if user_text:
        st.session_state["messages"].append(("user", user_text))  # 사용자 질문 저장
        with st.spinner("😊 답변을 생성 중입니다... 잠시만 기다려 주세요."):
            result = chain.invoke({"topic": user_text})   # 답변 생성
        st.session_state["messages"].append(("ai", result))    # 답변 저장
      
# 입력창과 버튼을 같은 줄에 배치
col1, col2 = st.columns([5,1])   # 두 개의 컬럼 생성 (비율 5:1)

with col1:
    topic = st.text_input("Topic:", placeholder="주제를 입력하세요...", key="input_box")
with col2:
    st.write("")   # 버튼을 입력창과 같은 높이에 맞추기 위해 빈 줄 추가
    st.write("")
    submit = st.button("질문하기", on_click=process_input) # 인수1 버튼 이름, 인수2 호출할 함수명
    
# 말풍선 (대화 기록 출력)
for role, text in st.session_state["messages"]: # 저장된 문자열(Human, AI 구분 출력)
    
    if role == "user": # 사용자 메세지 출력
        st.markdown(
            f"""
            <div style='text-align:right; margin:10px;'>
                <div style='display:inline-block; background:#DCF8C6; padding:12px; 
                            border-radius:15px; max-width:70%; color:black;'>
                    <b style='color:#075E54;'>🙋 사용자</b><br>{text}
                </div>
            </div>
            """,
            unsafe_allow_html = True # 스트림릿에서 HTML 태그를 그대로 렌더링(=출력) 
        )
    else: # AI 메세지 출력
        st.markdown(
            f"""
            <div style='text-align:left; margin:10px;'>
                <div style='display:inline-block; background:#E6E6E6; padding:12px;
                            border-radius:15px; max-width:70%; color:black;'>
                    <b style='color:#333;'>🤖 AI</b><br>{text}
                </div>
            </div>
            """,
            unsafe_allow_html = True 
        )



# (.venv) C:\workAI\work\LangChain\2.memory>streamlit run 9.streamlitTest.py
#   You can now view your Streamlit app in your browser.
#   Local URL: http://localhost:8501
#   Network URL: http://172.30.1.11:8501
