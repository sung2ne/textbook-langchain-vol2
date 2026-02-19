from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

llm = OllamaLLM(model="llama4")

rewrite_prompt = PromptTemplate(
    template="""다음 질문을 검색에 적합한 형태로 재작성하세요.
- 모호한 표현을 구체적으로 변경
- 대명사를 실제 명사로 대체
- 핵심 키워드 포함

원래 질문: {question}

재작성된 질문:""",
    input_variables=["question"]
)

chain = rewrite_prompt | llm


def rewrite_query(question: str) -> str:
    """쿼리 재작성"""
    result = chain.invoke({"question": question})
    return result.strip()


# 테스트
original = "그거 어떻게 쓰는 거야?"
rewritten = rewrite_query(original)
print(f"원본: {original}")
print(f"재작성: {rewritten}")
