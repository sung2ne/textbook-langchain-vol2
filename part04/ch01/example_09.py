contextual_prompt = PromptTemplate(
    template="""대화 기록을 참고하여 마지막 질문을 독립적인 검색 쿼리로 변환하세요.
대명사나 생략된 부분을 이전 대화에서 추론하여 완성하세요.

대화 기록:
{chat_history}

마지막 질문: {question}

독립적인 검색 쿼리:""",
    input_variables=["chat_history", "question"]
)


def contextualize_query(question: str, chat_history: list) -> str:
    """문맥 인식 쿼리 변환"""
    history_str = "\n".join([
        f"사용자: {h['user']}\nAI: {h['assistant']}"
        for h in chat_history
    ])

    chain = contextual_prompt | llm
    result = chain.invoke({
        "chat_history": history_str,
        "question": question
    })

    return result.strip()


# 테스트
chat_history = [
    {"user": "LangChain이 뭐야?", "assistant": "LangChain은 LLM 프레임워크입니다."},
    {"user": "어떤 기능이 있어?", "assistant": "체인, 에이전트, 메모리 등을 제공합니다."}
]
question = "그것 설치하는 방법은?"

contextualized = contextualize_query(question, chat_history)
print(f"원본: {question}")
print(f"변환: {contextualized}")
# 예: "LangChain 설치 방법"
