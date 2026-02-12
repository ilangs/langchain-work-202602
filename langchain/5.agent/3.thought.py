'''
1. cal.py
=> 함수(=기능)를 호출 => 개발자가 임의로(=필요할 때마다) 호출 (수동 호출)
=> 함수 호출 => AI 스스로 판단해서 스스로 호출 (자동 호출 => 개발자는 연결 (binding)) = tools(=도구들)
'''

from langchain_core.tools import tool

# 자동 호출
@tool # tool -> Decorate @tool가 붙어 있음 => 함수의 역할 문자열을 AI에게 전달하는 역할
def multiply(a: int, b: int): # 자료형 => 변수:자료형,,, => 자동으로 AI가 호출할 수 있도록 구현 @tool
    """ 두 정수를 곱하는 도구 입니다. """
    # 처리해야 할 업무
    return a * b

print(f"도구 이름: {multiply.name}") # 도구 이름을 출력(도구=함수 이름): multiply
print(f"도구 설명: {multiply.description}") # 도구 문제을 출력(도구=함수 문제): 두 정수를 곱하는 도구 입니다

# 함수 작성 ---> 연결(binding) -> 자동 호출
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# LLM 에게 우리가 만든 에이전트(=도구)가 있다는 것을 알려준다. 혛식) ~.bind_tools([함수명,함수명,,,])
llm_with_tools = llm.bind_tools([multiply])  # LLM이 호출할 대상 함수들을 알려준다.

# 테스트 호출
result = llm_with_tools.invoke("5 곱하기 3은?")
print(result.tool_calls) # LLM이 multply 도구(=에이전트)를 쓰겠다고 결정한 것을 볼 수 있다.


# 3. Thought loop

from langchain.agents import AgentExecutor, create_openai_functions_agent # 호출
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # 채팅 프롬프트

# 에이전트가 생각할 수 있는 가이드라인(Prompt) 설정
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 숫자 계산을 도와주는 유능한 AI 비서입니다."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # AI의 '생각의 흔적'을 담는 공간
])

# 에이전트 조립 (아직 실행 x => 내부 선언 (확인))
agent = create_openai_functions_agent(llm, [multiply], prompt) # 1.LLM객체, 2.tools[함수명], 3.Prompt (user가 전달)

# 실행 (agent executer) => Loop 핵심 (1.dpdlwjsxm wjdqh, 2.tools=[처리할 함수명], 3.verbose=True) # 처리 과정 (내부)(디버깅)
agent_executor = AgentExecutor(agent=agent, tools=[multiply], verbose=True)
agent_executor.invoke({"input":"123 곱하기 456을 계산 해 주세요."})


'''
도구 이름: multiply
도구 설명: 두 정수를 곱하는 도구 입니다.
[{'name': 'multiply', 'args': {'a': 5, 'b': 3}, 'id': 'call_6gFkhXQl7RKPi4k0iICV8nHx', 'type': 'tool_call'}]


> Entering new AgentExecutor chain...

Invoking: `multiply` with `{'a': 123, 'b': 456}`


56088123 곱하기 456은 56,088입니다.

> Finished chain.

'''