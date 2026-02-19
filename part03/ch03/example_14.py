from langchain.schema import BaseRetriever, Document
from typing import List


class CustomRetriever(BaseRetriever):
    """커스텀 Retriever"""

    vectorstore: any
    k: int = 5
    min_score: float = 0.5

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(self, query: str) -> List[Document]:
        """관련 문서 검색"""
        # 점수와 함께 검색
        results = self.vectorstore.similarity_search_with_relevance_scores(
            query,
            k=self.k * 2  # 필터링을 위해 더 많이 검색
        )

        # 점수 필터링
        filtered = [
            doc for doc, score in results
            if score >= self.min_score
        ]

        return filtered[:self.k]


# 사용
retriever = CustomRetriever(
    vectorstore=vectorstore,
    k=5,
    min_score=0.6
)

results = retriever.invoke("AI 도구")
