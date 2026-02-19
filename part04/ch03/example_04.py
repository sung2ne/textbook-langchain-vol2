from flashrank import Ranker, RerankRequest


class FlashReranker:
    """FlashRank 기반 리랭커"""

    def __init__(self, model_name: str = "ms-marco-MiniLM-L-12-v2"):
        self.ranker = Ranker(model_name=model_name)

    def rerank(self, query: str, documents: List[Document],
               top_k: int = 5) -> List[Tuple[Document, float]]:
        """문서 리랭킹"""
        # FlashRank 형식으로 변환
        passages = [
            {"id": i, "text": doc.page_content}
            for i, doc in enumerate(documents)
        ]

        # 리랭킹 요청
        rerank_request = RerankRequest(query=query, passages=passages)
        results = self.ranker.rerank(rerank_request)

        # 결과 변환
        doc_scores = []
        for result in results[:top_k]:
            doc_idx = result["id"]
            score = result["score"]
            doc_scores.append((documents[doc_idx], score))

        return doc_scores


# 사용
flash_reranker = FlashReranker()
reranked = flash_reranker.rerank(query, documents, top_k=3)
