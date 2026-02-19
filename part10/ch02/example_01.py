from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_ollama import OllamaLLM

# 도구 정의
def search(query: str) -> str:
    """웹 검색"""
    return f"'{query}' 검색 결과: ..."

def calculator(expression: str) -> str:
    """계산기"""
    return str(eval(expression))

tools = [
    Tool(name="search", func=search, description="웹 검색"),
    Tool(name="calculator", func=calculator, description="수학 계산")
]

# 에이전트 생성
llm = OllamaLLM(model="llama4")
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

# 실행
result = executor.invoke({"input": "서울 인구는 몇 명이고, 그 절반은?"})
