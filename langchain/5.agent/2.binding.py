'''
1. cal.py
=> 함수(=기능)를 호출 => 개발자가 임의로(=필요할 때마다) 호출 (수동 호출)
=> 함수 호출 => AI 스스로 판단해서 스스로 호출 (자동 호출 => 개발자는 연결 (binding)) = tools(=도구들)
'''

from langchain_core.tools import tool

# 사용자로 부터 값을 입력(매개변수)=>계산=>결과값(=반환값=return)

@tool # tool -> Decorate @tool가 붙어 있음 => 함수의 역할 문자열을 AI에게 전달하는 역할
def multiply(a: int, b: int): # 자료형 => 변수:자료형,,, => 자동으로 AI가 호출할 수 있도록 구현 @tool
    """ 두 정수를 곱하는 도구 입니다. """
    # 처리해야 할 업무
    return a * b

print(f"도구 이름: {multiply.name}") # 도구 이름을 출력(도구=함수 이름): multiply
print(f"도구 설명: {multiply.description}") # 도구 문제을 출력(도구=함수 문제): 두 정수를 곱하는 도구 입니다


# 2. 함수 작성 ---> 연결(binding) -> 자동 호출

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# LLM 에게 우리가 만든 에이전트(=도구)가 있다는 것을 알려준다. 혛식) ~.bind_tools([함수명,함수명,,,])
llm_with_tools = llm.bind_tools([multiply])  # LLM이 호출할 대상 함수들을 알려준다.

# 테스트 호출
result = llm_with_tools.invoke("5 곱하기 3은?")
print(result.tool_calls) # LLM이 multply 도구(=에이전트)를 쓰겠다고 결정한 것을 볼 수 있다.


'''
[{'name': 'multiply', 'args': {'a': 5, 'b': 3}, 'id': 'call_OvwIO4XDVhEzVmllRS0DsTif', 'type': 'tool_call'}]

'''