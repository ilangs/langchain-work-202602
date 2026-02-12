import streamlit as st     # Streamlit 라이브러리 불러오기 (웹 UI 제작용)
# 그림을 그려서 보여 준다, (도화지(Image), 붓(ImageDraw), 글씨체(ImageFont))
from PIL import Image, ImageDraw, ImageFont   # 화가 도구
import os # 파일 경로

# --- [요리 카드를 만드는 수동 호출 함수] ---
def draw_card(text):
    """ 주문받은 메뉴 이름을 넣어서 예쁜 요리카드를 그립니다."""

    #1. 도화지 생성 (가로 500px, 세로 300px) 크기의 RGB 크림색 배경
    img = Image.new("RGB", (500, 300), color=(255,255,240)) # 0~255*255*255
    
    #2. 붓 -> draw 객체를 생성
    draw = ImageDraw.Draw(img) # 도화지에 붓을 쥐고 그림
    
    #3. 폰트(글꼴) 선택: 한글이 깨지지 않게 준비한 폰트 파일을 불러옵니다.
    font_path = "./fonts/NotoSansCJKkr-Regular.otf"
    # 파일 불러올 때 예외처리 (1.파일 불러오기, 2.DB연동, 3.네트워크 프로그램)
    try:
        # 정상 처리 구문(1.적용시킬 폰트 경로, 2.폰트 크기 지정)
        font = ImageFont.truetype(font_path, 25)
    except:
        # 만약 폰트 파일이 없으면 에러 메시지를 띄우고 기본 폰트를 쓴다.
        st.error("폰트 파일을 찾을 수 없어요. 경로를 확인해주세요.")
        font = ImageFont.load_default()

    #4. 내용 쓰기 (1.글자위치, 2.출력글자, 3.글자색(빨간색), 4.적용폰트)
    draw.text((50, 130), f"오늘의 추천: {text}", fill=(255,0,0), font=font)
    
    #5. 테두리 장식 (1.x,y,w,h, 2.선 색깔, 3.선 굵기)
    draw.rectangle([10,10,490,290], outline=(100,100,100), width=3)
    
    #6. 파일로 완성: 그린 이미지를 'daily_card.png'라는 이름의 파일로 저장합니다.
    file_name = "./images/daily_card.png"
    img.save(file_name)
    
    return file_name  # 중간 점검: print(변수명 or 객체명) 또는 return 반환값

# --- [화면 구성] ---
st.title("🎨  요리사의 실제 카드 그리기") # h1~h2
st.write("요리사가 직접 손을 움직여 파일을 생성하는 단계입니다.")
# 사용자에게 메뉴 이름을 입력받습니다.
menu_name = st.text_input("추천할 메뉴 이름을 입력하세요 (예: 매콤 떡볶이)")

# 버튼을 누르면 요리사가 작업을 시작합니다.
if st.button("요리 카드 제작 시작!"): # 버튼을 누르면,
    st.spinner("⌛ 요리 카드 제작 중...")
    if menu_name: # 메뉴 이름이 존재한다면,
        # 7. 함수를 호출해서 파일을 실제로 만듭니다.
        path = draw_card(menu_name)
        # 8. 생성된 파일을 화면에 보여주기(1. 경로 포함한 불러올 이미지, 2.caption=타이틀 제목)
        st.image(path, caption="요리사가 방금 그린 따끈따끈한 카드")
        # 9. 파일이 실제 경로에 있는지 확인(check)
        if os.path.exists(path):
            st.success(f"성공! '{path}' 파일이 서버 폴더에 생성되었습니다.")
    else:
        st.warning("메뉴 이름을 먼저 입력해 주세요!")


