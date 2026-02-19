class StepBackRetriever:
    """Step-Back 기반 Retriever"""

    def __init__(self, vectorstore, llm):
        self.vectorstore = vectorstore
        self.llm = llm

    def invoke(self, question: str, k: int = 3):
        # 1. 원본 질문으로 검색
        original_results = self.vectorstore.similarity_search(question, k=k)

        # 2. Step-back 질문 생성
        general_question = step_back_query(question)

        # 3. 일반적 질문으로 검색
        general_results = self.vectorstore.similarity_search(general_question, k=k)

        # 4. 결과 결합 (중복 제거)
        seen = set()
        combined = []

        for doc in original_results + general_results:
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                combined.append(doc)

        return combined[:k]
