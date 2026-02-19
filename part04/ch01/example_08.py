decompose_prompt = PromptTemplate(
    template="""다음 복잡한 질문을 답변하기 위해 필요한 하위 질문들로 분해하세요.
각 하위 질문은 독립적으로 검색 가능해야 합니다.
3-5개의 하위 질문을 생성하세요.

복잡한 질문: {question}

하위 질문들:""",
    input_variables=["question"]
)


def decompose_query(question: str) -> list[str]:
    """질문 분해"""
    chain = decompose_prompt | llm
    result = chain.invoke({"question": question})

    # 파싱
    lines = result.strip().split("\n")
    sub_questions = []

    for line in lines:
        # 번호나 불릿 제거
        cleaned = line.strip().lstrip("0123456789.-) ")
        if cleaned:
            sub_questions.append(cleaned)

    return sub_questions


# 테스트
complex_question = "RAG 시스템을 구축하려면 어떤 기술이 필요하고 각각 어떻게 구현하나요?"
sub_questions = decompose_query(complex_question)

print(f"원본: {complex_question}")
print("\n하위 질문:")
for i, q in enumerate(sub_questions, 1):
    print(f"  {i}. {q}")
