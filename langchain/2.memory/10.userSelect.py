from callFunction import *

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2) 

# 사용자 선택에 따라 사용할 프롬프트 템플릿 정의
prompt_map = {
    "1": ("요약", "다음 내용을 한 문장으로 요약 해 주세요\n 내용 {text}"),
    "2": ("키워드", "다음 내용에서 핵심 키워드 5개를 뽑아 주세요\n 내용 {text}"),
    "3": ("답변", "다음 질문에 3문장 이내로 답변 해 주세요\n 내용 {text}"),
}

# 처리방식 선텍 메뉴
print("1. 요약, 2. 키워드, 3. 3문장 이내 답변")

sel = input("선택(1~3): ").strip()

if sel not in prompt_map:
    raise SystemExit("잘못된 선택")

name, template = prompt_map[sel]
prompt = ChatPromptTemplate.from_template(template)
# print("name, template=>", name, template)

chain = prompt | llm | StrOutputParser()

text = input(f"[{name}] 입력: ").strip()
print(chain.invoke(text))


'''
1. 요약, 2. 키워드, 3. 3문장 이내 답변
선택(1~3): 1
[요약] 입력: 랭체인
"랭체인"은 자연어 처리 및 AI 모델을 활용하여 다양한 애플리케이션을 개발하고 운영하는 프레임워크입니다.
'''

'''
1. 요약, 2. 키워드, 3. 3문장 이내 답변
선택(1~3): 2
[키워드] 입력: REST API를 식당의 메뉴판에 비유해 볼 수 있습니다. 식당에 가면 메뉴판을 보고 원하는 음식을 주문하는 것과 유샤합니다. 
1. REST API
2. 식당
3. 메뉴판
4. 주문
5. 음식
'''






