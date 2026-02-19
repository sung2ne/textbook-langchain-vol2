from langgraph.graph import StateGraph, END

# 상태 정의
class AgentState:
    messages: list
    next_step: str

# 그래프 생성
graph = StateGraph(AgentState)

# 노드 추가
graph.add_node("research", research_node)
graph.add_node("analyze", analyze_node)
graph.add_node("write", write_node)

# 엣지 추가
graph.add_edge("research", "analyze")
graph.add_edge("analyze", "write")
graph.add_edge("write", END)

# 컴파일
chain = graph.compile()
