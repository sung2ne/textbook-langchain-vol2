# 연구원 에이전트
researcher = Agent(
    role="연구원",
    goal="정보 수집",
    tools=[search_tool, web_scraper]
)

# 작성자 에이전트
writer = Agent(
    role="작성자",
    goal="보고서 작성",
    tools=[document_tool]
)

# 검토자 에이전트
reviewer = Agent(
    role="검토자",
    goal="품질 검토",
    tools=[grammar_tool, fact_checker]
)

# 팀 구성
team = [researcher, writer, reviewer]
