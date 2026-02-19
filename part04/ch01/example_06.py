stepback_prompt = PromptTemplate(
    template="""다음 구체적인 질문을 더 일반적인 질문으로 변환하세요.
배경 지식을 얻을 수 있는 넓은 범위의 질문을 만드세요.

구체적 질문: {question}

일반적 질문:""",
    input_variables=["question"]
)


def step_back_query(question: str) -> str:
    """질문 추상화"""
    chain = stepback_prompt | llm
    return chain.invoke({"question": question}).strip()


# 테스트
specific = "LangChain에서 ChromaDB 연동 시 에러 해결법"
general = step_back_query(specific)

print(f"구체적: {specific}")
print(f"일반적: {general}")
# 예: "LangChain과 벡터 데이터베이스 연동 방법"
