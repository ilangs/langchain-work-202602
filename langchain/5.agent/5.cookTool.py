'''
5. cookTool.py (기능 추가)
'''

import streamlit as st                   # Streamlit 라이브러리 불러오기 (웹 UI 제작용)
from langchain_openai import ChatOpenAI  # OpenAI 기반 LLM(ChatGPT) 연결용
from langchain.tools import tool         # LangChain에서 도구를 정의할 수 있는 데코레이터 불러오기
from dotenv import load_dotenv           # 환경변수(.env 파일) 불러오기

load_dotenv()    # .env 파일에 저장된 API 키 등 환경변수 로드

# ------------------------------------------------------------------------------------------
# [1단계] 요리사가 쓸 수 있는 '도구'들의 설명서 만들기
# ------------------------------------------------------------------------------------------
@tool  # LangChain이 인식할 수 있도록 도구로 등록
def check_ingredient_price(item_name: str):  # 재료 가격을 조회하는 도구 정의
    """ 식재료의 현재 시장 가격을 조회합니다. 식재료 이름이 입력되어야 합니다."""  # 기능 설명 + 매개변수 설정
    return f"[{item_name}] 의 가격은 오늘 시세로 5,000원입니다."  # 실제 동작 대신 설명 문자열 반환

@tool  # 다른 도구 정의
def get_recipe(food_name: str):  # 음식 레시피를 조회하는 도구 정의
    """특정 음식의 조리법(레시피)을 검색합니다. 음식이름이 입력되어야 합니다."""  # 기능 설명 + 매개변수 설정
    return f"{food_name} 레시피: 먼저 재료를 손질하고 냄비에 넣으세요..."  # 실제 동작 대신 설명 문자열 반환

@tool # 칼 갈기 도구 추가!
def sharpen_knife(knife_type: str):
    """ 잘 들지 않는 칼을 날카롭게 갑니다. 칼의 종류(식칼, 과도 등)를 알려주면 더 좋습니다."""
    return f"{knife_type}을 아주 날카롭게 갈았습니다. 이제 요리 준비가 끝났습니다!"

@tool
def check_ingredient_price(item_name : str):
    """ 식재료의 현재 시장 가격을 조회합니다. 식재료 이름이 입력되어야 합니다."""
    #함수의 기능
    return f" {item_name} 의 가격은 오늘 시세로 5,000원 입니다."

# ------------------------------------------------------------------------------------------
# [2단계] 요리사(LLM) 와 연장통 연결하기
# 요리사의 '뇌'를 준비합니다 (GPT-4o-mini 사용), emperature=0으로 정확한 응답 설정
# ------------------------------------------------------------------------------------------

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  

# 이게 바로 핵심! bind_tools! 
# 요리사에게 "너는 이제 가격 조회, 레시피 검색, 칼 갈기도 할 줄 알아"라고 교육시킵니다.

tools_list = [check_ingredient_price, get_recipe, sharpen_knife]
chef_with_tools = llm.bind_tools(tools_list) 

# ------------------------------------------------------------------------------------------
# [3단계] 웹 화면 구성 및 판단 결과 보기
# ------------------------------------------------------------------------------------------
st.title("👨‍🍳 심화: 새로운 연장(칼 갈기) 테스트")
st.write("요리사에게 '칼이 너무 무뎌졌어'라고 말해보거나 '고기 가격 알려줘'라고 해보세요.")
# 사용자 입력창
order = st.text_input("요리사에게 할 말을 입력하세요:")

# 판단 결과 보기
if order:
    # 요리사가 사용자의 말을 듣고 고민합니다 (invoke)
    response = chef_with_tools.invoke(order) # LLM이 입력을 받아 응답 생성
    
    # 요리사가 어떤 도구를 쓰기로 결심했는지 확인합니다.
    if response.tool_calls:    # 응답에 도구 호출 계획이 포함되어 있다면
        # AI가 선택한 도구의 이름을 가져옵니다.
        chosen_tool = response.tool_calls[0]['name']
        st.success(f"🎯 요리사의 판단: 지금 필요한 건 '{chosen_tool}' 직원 호출이네요")
        # 상세한 판단 근거(JSON)를 보여줍니다.
        st.json(response.tool_calls)  
    else:
        st.info("💡 요리사의 판단: 이건 그냥 대화로 충분해요. 직원을 부를 필요는 없겠네요!")
        # 도구가 필요 없을 경우 메시지 출력
        st.write(response.content)



# (.venv) C:\workAI\work\LangChain\5.agent>streamlit run 5.cookTool.py

# 👨‍🍳 심화: 새로운 연장(칼 갈기) 테스트
# 요리사에게 '칼이 너무 무뎌졌어'라고 말해보거나 '고기 가격 알려줘'라고 해보세요.

# 요리사에게 할 말을 입력하세요:
# 돼지고기 가격 알려줘

# 🎯 요리사의 판단: 지금 필요한 건 'check_ingredient_price' 도구군!

# [
# 0:{
# "name":"check_ingredient_price"
# "args":{
# "item_name":"돼지고기"
# }
# "id":"call_N6oHIfoJFQW3mTQ2C2JcgUSV"
# "type":"tool_call"
# }
# ]

# 요리사에게 할 말을 입력하세요:
# 비빔밥

# 🎯 요리사의 판단: 지금 필요한 건 'get_recipe' 도구군!

# [
# 0:{
# "name":"get_recipe"
# "args":{
# "food_name":"비빔밥"
# }
# "id":"call_s5l0GDk9cj55zg3JVPyrbQtN"
# "type":"tool_call"
# }
# ]

# 요리사에게 할 말을 입력하세요:
# 칼이 너무 무뎌졌어

# 💡 요리사의 판단: 이건 도구가 필요 없는 일반적인 대화네요.

# 어떤 종류의 칼을 날카롭게 하고 싶으신가요? (예: 식칼, 과도 등)

# 요리사에게 할 말을 입력하세요:
# 식칼

# 🎯 요리사의 판단: 지금 필요한 건 'sharpen_knife' 도구군!

# [
# 0:{
# "name":"sharpen_knife"
# "args":{
# "knife_type":"식칼"
# }
# "id":"call_pkJEYaHgLeTuyUlTJmUhmuhd"
# "type":"tool_call"
# }
# ]
