from langchain.schema import BaseRetriever, Document
from typing import List
import numpy as np


class HybridRetriever(BaseRetriever):
    """커스텀 하이브리드 검색기"""

    bm25_retriever: any
    vector_retriever: any
    bm25_weight: float = 0.5
    k: int = 5

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(self, query: str) -> List[Document]:
        # BM25 검색
        bm25_results = self.bm25_retriever.invoke(query)

        # 벡터 검색
        vector_results = self.vector_retriever.invoke(query)

        # 점수 계산 및 결합
        doc_scores = {}

        # BM25 점수 (순위 기반)
        for i, doc in enumerate(bm25_results):
            key = doc.page_content
            score = self.bm25_weight * (1 / (i + 1))
            doc_scores[key] = doc_scores.get(key, 0) + score

        # 벡터 점수 (순위 기반)
        vector_weight = 1 - self.bm25_weight
        for i, doc in enumerate(vector_results):
            key = doc.page_content
            score = vector_weight * (1 / (i + 1))
            doc_scores[key] = doc_scores.get(key, 0) + score

        # 정렬
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

        # Document 객체 재구성
        content_to_doc = {doc.page_content: doc for doc in bm25_results + vector_results}
        results = [content_to_doc[content] for content, score in sorted_docs[:self.k]]

        return results


# 사용
hybrid = HybridRetriever(
    bm25_retriever=bm25_retriever,
    vector_retriever=vector_retriever,
    bm25_weight=0.4,
    k=5
)

results = hybrid.invoke("LangChain 프레임워크")
