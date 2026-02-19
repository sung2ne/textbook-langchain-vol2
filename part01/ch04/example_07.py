import numpy as np
from typing import Optional


class EmbeddingUtils:
    """임베딩 유틸리티"""

    def __init__(self, embeddings):
        self.embeddings = embeddings

    def cosine_similarity(self, vec1, vec2):
        """코사인 유사도"""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def find_most_similar(self, query: str, documents: list[str],
                          top_k: int = 3, threshold: float = 0.0):
        """가장 유사한 문서 찾기"""
        query_vec = self.embeddings.embed_query(query)
        doc_vecs = self.embeddings.embed_documents(documents)

        results = []
        for i, doc_vec in enumerate(doc_vecs):
            sim = self.cosine_similarity(query_vec, doc_vec)
            if sim >= threshold:
                results.append({
                    "index": i,
                    "document": documents[i],
                    "similarity": sim
                })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def deduplicate(self, documents: list[str], threshold: float = 0.95):
        """중복 문서 제거"""
        if not documents:
            return []

        vectors = self.embeddings.embed_documents(documents)
        unique_docs = [documents[0]]
        unique_vecs = [vectors[0]]

        for i in range(1, len(documents)):
            is_duplicate = False
            for unique_vec in unique_vecs:
                sim = self.cosine_similarity(vectors[i], unique_vec)
                if sim >= threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_docs.append(documents[i])
                unique_vecs.append(vectors[i])

        return unique_docs

    def cluster_by_similarity(self, documents: list[str], threshold: float = 0.7):
        """유사도 기반 클러스터링"""
        if not documents:
            return []

        vectors = self.embeddings.embed_documents(documents)
        clusters = []
        assigned = [False] * len(documents)

        for i in range(len(documents)):
            if assigned[i]:
                continue

            cluster = [i]
            assigned[i] = True

            for j in range(i + 1, len(documents)):
                if assigned[j]:
                    continue

                sim = self.cosine_similarity(vectors[i], vectors[j])
                if sim >= threshold:
                    cluster.append(j)
                    assigned[j] = True

            clusters.append({
                "indices": cluster,
                "documents": [documents[idx] for idx in cluster]
            })

        return clusters


# 사용 예시
embeddings = OllamaEmbeddings(model="nomic-embed-text")
utils = EmbeddingUtils(embeddings)

# 유사 문서 찾기
documents = [
    "파이썬 프로그래밍 기초",
    "Python 입문 가이드",
    "자바스크립트 튜토리얼",
    "파이썬으로 웹 개발하기",
]

results = utils.find_most_similar("파이썬 배우기", documents, top_k=2)
for r in results:
    print(f"[{r['similarity']:.3f}] {r['document']}")

# 중복 제거
unique = utils.deduplicate(documents, threshold=0.8)
print(f"원본: {len(documents)}개 → 중복 제거: {len(unique)}개")
