expansion_prompt = PromptTemplate(
    template="""다음 질문을 다양한 관점에서 3개의 검색 쿼리로 확장하세요.
각 쿼리는 한 줄에 하나씩 작성하세요.

원래 질문: {question}

확장된 쿼리:""",
    input_variables=["question"]
)

expand_chain = expansion_prompt | llm


def expand_query(question: str) -> list[str]:
    """쿼리 확장"""
    result = expand_chain.invoke({"question": question})
    queries = [q.strip() for q in result.strip().split("\n") if q.strip()]
    return queries[:3]


# 테스트
question = "RAG 성능을 높이려면?"
expanded = expand_query(question)
print(f"원본: {question}")
print("확장:")
for i, q in enumerate(expanded, 1):
    print(f"  {i}. {q}")
