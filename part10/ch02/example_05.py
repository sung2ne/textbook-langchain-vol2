# RAG 에이전트
rag_agent = Agent(
    tools=[
        retriever_tool,    # 문서 검색
        web_search_tool,   # 웹 검색
        calculator_tool    # 계산
    ],
    strategy="adaptive_rag"
)
