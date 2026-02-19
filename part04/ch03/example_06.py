import numpy as np


class DiverseReranker:
    """다양성 고려 리랭커"""

    def __init__(self, base_reranker, embeddings, diversity_weight: float = 0.3):
        self.base_reranker = base_reranker
        self.embeddings = embeddings
        self.diversity_weight = diversity_weight

    def rerank(self, query: str, documents: List[Document],
               top_k: int = 5) -> List[Tuple[Document, float]]:
        """다양성 고려 리랭킹"""
        # 기본 리랭킹
        base_results = self.base_reranker.rerank(query, documents, top_k=len(documents))

        # 문서 임베딩
        doc_embeddings = self.embeddings.embed_documents(
            [doc.page_content for doc, _ in base_results]
        )

        # MMR 스타일 선택
        selected = []
        selected_indices = set()

        while len(selected) < top_k and len(selected) < len(base_results):
            best_idx = -1
            best_score = -float("inf")

            for i, (doc, rel_score) in enumerate(base_results):
                if i in selected_indices:
                    continue

                # 다양성 점수 (선택된 문서들과의 최대 유사도)
                if selected:
                    similarities = [
                        np.dot(doc_embeddings[i], doc_embeddings[j])
                        for j in selected_indices
                    ]
                    max_sim = max(similarities)
                    diversity_score = 1 - max_sim
                else:
                    diversity_score = 1

                # 최종 점수
                final_score = (
                    (1 - self.diversity_weight) * rel_score +
                    self.diversity_weight * diversity_score
                )

                if final_score > best_score:
                    best_score = final_score
                    best_idx = i

            if best_idx >= 0:
                selected.append((base_results[best_idx][0], best_score))
                selected_indices.add(best_idx)

        return selected


# 사용
diverse_reranker = DiverseReranker(
    CrossEncoderReranker(),
    OllamaEmbeddings(model="nomic-embed-text"),
    diversity_weight=0.3
)
