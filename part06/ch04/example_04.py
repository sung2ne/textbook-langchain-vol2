from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.documents import Document


class HybridSearchOptimizer:
    """하이브리드 검색 최적화"""

    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def create_hybrid_retriever(self, documents: List[Document],
                               weights: tuple = (0.5, 0.5)) -> EnsembleRetriever:
        """하이브리드 리트리버 생성"""
        # 벡터 검색
        vector_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

        # BM25 검색
        bm25_retriever = BM25Retriever.from_documents(documents)
        bm25_retriever.k = 5

        # 앙상블
        ensemble = EnsembleRetriever(
            retrievers=[vector_retriever, bm25_retriever],
            weights=list(weights)
        )

        return ensemble

    def find_optimal_weights(self, documents: List[Document],
                            test_queries: List[Dict]) -> tuple:
        """최적 가중치 탐색"""
        best_weights = (0.5, 0.5)
        best_score = 0

        for vector_weight in [0.3, 0.4, 0.5, 0.6, 0.7]:
            bm25_weight = 1.0 - vector_weight
            weights = (vector_weight, bm25_weight)

            retriever = self.create_hybrid_retriever(documents, weights)

            # 평가
            score = self._evaluate_retriever(retriever, test_queries)

            if score > best_score:
                best_score = score
                best_weights = weights

            print(f"가중치 {weights}: 점수 {score:.2f}")

        return best_weights

    def _evaluate_retriever(self, retriever, test_queries: List[Dict]) -> float:
        """리트리버 평가"""
        hits = 0

        for query_data in test_queries:
            query = query_data["query"]
            relevant = set(query_data.get("relevant_docs", []))

            results = retriever.get_relevant_documents(query)
            retrieved = set(doc.metadata.get("id", "") for doc in results)

            if retrieved & relevant:
                hits += 1

        return hits / len(test_queries) if test_queries else 0
