from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough


def generate_hypothetical_answer(question: str) -> str:
    """가상 답변 생성"""
    prompt = PromptTemplate(
        template="""다음 질문에 대한 가상의 답변을 작성하세요.
실제 정보가 아니어도 됩니다. 관련 키워드를 포함한 답변을 생성하세요.

질문: {question}

가상 답변:""",
        input_variables=["question"]
    )

    chain = prompt | llm
    return chain.invoke({"question": question})


class HyDERetriever:
    """HyDE 기반 Retriever"""

    def __init__(self, vectorstore, llm):
        self.vectorstore = vectorstore
        self.llm = llm
        self.embeddings = vectorstore._embedding_function

    def invoke(self, question: str, k: int = 3):
        # 1. 가상 답변 생성
        hypothetical = generate_hypothetical_answer(question)

        # 2. 가상 답변으로 검색
        results = self.vectorstore.similarity_search(hypothetical, k=k)

        return results


# 사용
hyde_retriever = HyDERetriever(vectorstore, llm)
results = hyde_retriever.invoke("RAG가 뭐야?")

for doc in results:
    print(f"- {doc.page_content}")
