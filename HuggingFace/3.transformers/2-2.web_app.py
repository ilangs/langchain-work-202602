# 🎨 2단계: Streamlit 웹 화면 코드 (5.web_app.py)
# 사용자가 브라우저에서 텍스트를 입력하고 버튼을 누르면 입력된 텍스트는 FastAPI 서버로 전송됨.

import streamlit as st
import requests

# FastAPI 서버 주소 (로컬에서 실행 시 기본 주소)
API_URL = "http://localhost:8000/predict"

# 1. 화면 구성 (디자인)
st.set_page_config(page_title="AI 스팸 필터링", page_icon="🛡️")

st.title("🛡️ AI 스팸 문자 필터링 서비스")
st.write("의심되는 문자 메시지 내용을 아래에 입력해 보세요. AI가 스팸 여부를 판별해 줍니다.")

# 2. 사용자 입력 창
user_input = st.text_area("문자 내용 입력:", height=150, placeholder="여기에 문자를 붙여넣으세요...")

# 3. 판별 버튼 클릭 시 동작
if st.button("🚨 스팸 검사하기", use_container_width=True):
    if user_input.strip() == "":
        st.warning("문자 내용을 입력해주세요!")
    else:
        with st.spinner("AI가 문맥을 분석 중입니다..."):
            try:
                # FastAPI 서버로 데이터 전송
                response = requests.post(API_URL, json={"text": user_input})
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 결과 화면 출력
                    st.divider()
                    if result["is_spam"]:
                        st.error(f"⚠️ **위험!** 이 문자는 **스팸**일 확률이 **{result['confidence']}%** 입니다.")
                    else:
                        st.success(f"✅ **안전!** 이 문자는 **정상**일 확률이 **{result['confidence']}%** 입니다.")
                else:
                    st.error("서버에서 오류가 발생했습니다. (FastAPI 서버가 켜져 있는지 확인하세요)")
                    
            except requests.exceptions.ConnectionError:
                st.error("API 서버에 연결할 수 없습니다. 터미널에서 FastAPI 서버를 먼저 실행해 주세요!")
