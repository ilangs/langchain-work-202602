# frontend_ui.py

import streamlit as st                      # 웹UI 구성
import requests,os,time,textwrap            # http 요청, 시스템 접근, 시간측정, 텍스트 줄바꿈
import pandas as pd                         # 통계 및 데이터프레임 처리
from io import BytesIO                      # 메모리 기반 바이너리 버퍼(이미지를 처음부터 메모리에 저장)
from PIL import Image,ImageDraw,ImageFont   # 도화지,붓,글자체 (이미지 생성 및 텍스트)
from gtts import gTTS                       # 텍스트를 음성으로 변환
# 추가
from langsmith import Client                # LangSmith 클라이언트 (추적 및 분석용)

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv()

# 리소스 캐싱 => @st.cache_resource 옵션 (메모리에서 불러올 때 속도 향상)
@st.cache_resource
def get_langsmith_client():
    """ LangSmith 클라이언트를 싱글톤으로 캐싱 """
    return Client()      # 익명 객체 vs cl = Clint() -> return cl

@st.cache_resource
def load_global_fonts():
    """ 운영체제에 따라 한글 폰트 경로를 캐싱 """
    # nt=>window OS, 윈도우(맑은고딕) 아니면 리눅스(나눔고딕)
    fpath = "C:/Windows/Fonts/malgun.ttf" if os.name == 'nt' else \
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    if not os.path.exists(fpath):
        return None     # 폰트가 없으면 기본 폰트 사용
    return fpath

# 전역 리소스 초기화
ls_client = get_langsmith_client()  # LangSmith 클라이언트 객체 생성
font_path = load_global_fonts()     # 폰트 경로 설정

PROJECT_NAME = os.environ.get("LANGCHAIN_PROJECT")  # 프로젝트 이름은 키값으로 불러온다.

# 메모리 효율화(이미지 캐싱)
# @st.cache_data => streamlit의 데이터 캐싱 데코레이터(과정 생략 -> 결과만 받고 싶을 때)
# 함수를 실행할 때 입력매개변수와 결과를 저장(cache)하여, 동일한 요청시 결과만 즉시 반환 
@st.cache_data(show_spinner=False)   # 로딩 중임을 알리는 회전 아이콘 화면표시 여부 -> 백그라운드 실행
def create_report_image_cached(text):
    """ 텍스트를 이미지로 변환하고 캐싱하여 성능을 최적화시키 함수 """
    img = Image.new('RGB',(800,750),color=(255,255,255))  # 흰색 도화지 생성
    draw = ImageDraw.Draw(img)   # 이미지에 텍스트를 넣어주는 도구로써 사용
    
    # 폰트 설정 (경로,크기)
    try:
        font = ImageFont.truetype(font_path,18) if font_path else ImageFont.load_default()
        t_font = ImageFont.truetype(font_path,28) if font_path else ImageFont.load_default()
    except:
        font = ImageFont.load_default(); t_font = font   # 명령어1; 명령어2; 명령어3;
        
    # 테두리 및 제목 삽입(-20 축소)
    draw.rectangle([20,20,780,730],outline=(0,51,153),width=3)   # 테두리 색, 굵기:3
    draw.text((40,40)," AI 전문가 최종 리포트", font=t_font, fill=(0,51,153))
    
    # 본문 텍스트 삽입(줄바꿈 처리)
    y_pos = 100
    for line in textwrap.wrap(text, width=45):  # 여백 주면서 줄바꿈
        draw.text((40,y_pos), line, font=font, fill=(40,40,40)) # 0~255
        y_pos += 30
        
    # 이미지를 버퍼 반환 (속도)
    # buf.seek(0): 읽기 순서(위치) 0->1,2,3,,,257 => 다음번 이미지를 빨리 읽기 위해 위치를 0으로 설정
    buf = BytesIO(); img.save(buf, format="PNG"); buf.seek(0) # 0 위치로 이동
    return buf.getvalue()

# Streamlit 페이지 설정
st.set_page_config(page_title = "Expert Admin V13", layout = "wide")

# 새로고침 => 맨처음부터 다시 읽어들임 => 세션처리
if "chat_history" not in st.session_state: st.session_state.chat_history = []  # 대화기록
if "late_ans" not in st.session_state: st.session_state.late_ans = []  # 마지막 답변
if "stats_log" not in st.session_state: st.session_state.stats_log = []  # 통계로그

# 화면 디자인
menu = st.sidebar.radio("업무 상태",["전문가 상담실", "운영 통계 대시보드"])

# 메뉴1: 전문가 상담실
if menu == "전문가 상담실":
    st.title("실시간 통합 상담 센터(Front-end Optimized)")
    #1.이전 채팅내역 출력
    for role, content in st.session_state.chat_history:  #[] 누가(role), 대화내용(content)
        with st.chat_message(role): st.write(content)
        
    #2.사용자 질문 입력 및 처리
    if prompt:= st.chat_input("질문을 입력하세요..."):
        st.session_state.chat_history.append(("user", prompt)) # 사용자 질문 저장
        with st.chat_message("user"): st.write(prompt)
        
        with st.spinner("백엔드 엔진에서 지식을 추출 중입니다..."):
            # FastAPI 백엔드에 post 요청 (Query Parameter로 매개변수를 전달한다.)
            res = requests.post(f"http://127.0.0.1:8000/ask?query={prompt}")
            # 서버로부터 응답을 받았다면 (상태코드가 200 ok)
            if res.status_code == 200:
                data = res.json()       # 전달 반환 받은 값은 json( {키명:값, ,,,} )
                st.session_state.late_ans = data["answer"]                          # 답변 저장
                st.session_state.chat_history.append(("assistant", data["answer"])) # 답변 출력
                st.session_state.stats_log.append(data["stats"])                    # 통계 저장
                st.rerun()                                                          # UI 새로 고침

    #3.답변 시각화 (이미지 + 음성)
    if st.session_state.late_ans:
        st.divider() 
        col1, col2 = st.columns(2) # 반환값을 각각 나누어서 받을 수 있다.
        
        # 이미지 카드 생성 및 다운로드
        with col1:
            # 항상 서버에게 질문할 때 맨 마지막 질문
            img_bytes = create_report_image_cached(st.session_state.late_ans)
            st.image(img_bytes)         # st.image(메모상의 그림) => 화면에 출력
            st.download_button("이미지 저장", img_bytes, "report.png", key="btn_img")
        
        # 음성 변환 및 다운로드
        with col2:
            tts = gTTS(text=st.session_state.late_ans[:300], lang='ko')   # 300자 제한
            v_buf = BytesIO(); tts.write_to_fp(v_buf); v_buf.seek(0)  # 0 위치로 이동
            st.audio(v_buf.getvalue())  # 음성 play bar (~.mp3 저장)
            st.download_button("MP3 저장", v_buf.getvalue(), "voice.mp3", key="btn_aud")
    
# 메뉴2: 운영 통계 대시보드
elif menu == "운영 통계 대시보드":   #랭스미스
    st.title("통합 운영 관제")
    
    # 통계 데이터가 있는 경우
    if st.session_state.stats_log:
        df = pd.DataFrame(st.session_state.stats_log)  # 세션값을 표 형태로 저장(분석 목적)
        # KPI 지표 출력
        m1,m2,m3 = st.columns(3)
        m1.metric("평균 지연 시간", f"{df['latency'].mean():.2f} sec")  # 소수점 2자리
        m2.metric("총 토큰 사용량", f"{df['total_tokens'].sum():,} tkn") 
        m3.metric("누적 운용 비용", f"{df['total_cost'].sum():,.5f} ")
        
        st.divider()
        st.line_chart(df.set_index("timestamp")["latency"])  # 지연시간 추이 표
        st.dataframe(df, use_container_width=True) # 전체 로그 출력
       
    # 통계 데이터가 없는 경우
    else:
        st.info("통계 데이터가 없습니다.")
