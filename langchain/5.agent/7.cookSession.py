# 7.cookSession.py

import streamlit as st    # Streamlit 라이브러리 불러오기 (웹 UI 제작용)
# 그림을 그려서 보여 준다, (도화지(Image), 붓(ImageDraw), 글씨체(ImageFont))
from PIL import Image, ImageDraw, ImageFont   # 화가 도구
import os # 파일 경로

# ---------------------------------------------------------------------------------
# [1단계] 냉장고(=보관함)가 비어있다면 칸을 마련합니다. => 세션 id값을 미리 정해 놓음
# ---------------------------------------------------------------------------------
# 페이지가 처음 열릴 때 딱 한 번만 실행되는 설정 => st.session_state vs class 에서의 저장
if "my_fridge" not in st.session_state:
    # 이미지 데이터와 메뉴 이름을 담을 빈 칸을 만듭니다.
    st.session_state.my_fridge = {"img_data": None, "menu_name": "없음"}

st.title("📥 요리사의 신선 보관함 실습")
st.write("버튼을 눌러도 데이터가 사라지지 않는 '금고'의 원리")

# ---------------------------------------------------------------------------------
# [2단계] 기능을 확인하면서 요리를 만드는 작업
# ---------------------------------------------------------------------------------
menu_input = st.text_input("냉장고에 넣을 메뉴 이름을 입력하세요:")

if st.button("요리 완성 및 냉장고 보관!"): # 버튼을 누르면,
    if menu_input: # 메뉴 이름이 존재한다면,
        img = Image.new("RGB", (400,200), color=(255,255,200))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("./fonts/NotoSansCJKkr-Regular.otf", 25)
        except:
            font = ImageFont.load_default()
            
        draw.text((50, 80), f"신선 보관{menu_input}", fill=(0,0,0), font=font)
        img.save("./images/temp_dish.png") # 파일로 저장
        
        ######## [핵심] 생성된 파일을 냉장고(session_state)에 저장 ############################
        
        # with open(1.불러올 경로 포함 파일명, 2.불러오는 모드) as 별칭:
        with open("./images/temp_dish.png", "rb") as f: # rb = read binary
            # 파일을 냉장고에 저장 (키명(대문자,소문자 구분))
            st.session_state.my_fridge["img_data"] = f.read() #img_data 키값에 이미지 저장 완료
            st.session_state.my_fridge["menu_name"] = menu_input
        
        ###################################################################################

        st.success(f"'{menu_input}' 요리를 냉장고에 보관 완료 !!!")
    else:
        st.warning("메뉴 이름을 먼저 입력해 주세요!")

# ---------------------------------------------------------------------------------
# [3단계] 냉장고에서 꺼내서 손님에게 보여주기
# ---------------------------------------------------------------------------------
# 이 부분은 페이지가 새로고침되어도 'my_fridge' 안에 데이터가 있다면 항상 실행된다.
if st.session_state.my_fridge["img_data"]:
    st.divider() # 구분선
    st.subheader(f"🧺 냉장고에서 꺼낸 요리: {st.session_state.my_fridge['menu_name']}")
    
    # 냉장고(=session_state)에 보관된 바이트 데이터를 이미지로 그대로 보여준다.(=직렬화)
    st.image(st.session_state.my_fridge["img_data"])
    
    # 다운로드 버튼도 냉장고에 있는 데이터를 그대로 사용하므로 링크가 사라지지 않음.
    st.download_button(
        label="📸 요리 카드 사진 저장",                # 버튼의 타이틀 제목
        data=st.session_state.my_fridge["img_data"], # 연관된 데이터 표시
        file_name="chef_recipe_card.png",            # 디운로드 파일명
        mime="image/png"                             # 다운로드 파일 타입 (img/확장자 종류)
    )
    # 새로 고침의 문제점 => streamlit은 코드 한줄만 바꿔도 위에서부터 다시 실행
else:
    st.warning("보관된 요리가 없습니다.!")
    

