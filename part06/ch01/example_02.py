from typing import List, Dict
import numpy as np


class RetrievalMetrics:
    """검색 평가 지표"""

    def precision_at_k(self, retrieved: List[str], relevant: List[str], k: int) -> float:
        """Precision@K"""
        retrieved_k = set(retrieved[:k])
        relevant_set = set(relevant)

        if not retrieved_k:
            return 0.0

        return len(retrieved_k & relevant_set) / len(retrieved_k)

    def recall_at_k(self, retrieved: List[str], relevant: List[str], k: int) -> float:
        """Recall@K"""
        retrieved_k = set(retrieved[:k])
        relevant_set = set(relevant)

        if not relevant_set:
            return 0.0

        return len(retrieved_k & relevant_set) / len(relevant_set)

    def f1_at_k(self, retrieved: List[str], relevant: List[str], k: int) -> float:
        """F1@K"""
        p = self.precision_at_k(retrieved, relevant, k)
        r = self.recall_at_k(retrieved, relevant, k)

        if p + r == 0:
            return 0.0

        return 2 * p * r / (p + r)

    def mrr(self, retrieved: List[str], relevant: List[str]) -> float:
        """MRR"""
        relevant_set = set(relevant)

        for i, doc in enumerate(retrieved):
            if doc in relevant_set:
                return 1.0 / (i + 1)

        return 0.0

    def hit_rate(self, retrieved: List[str], relevant: List[str], k: int) -> float:
        """Hit Rate@K (적어도 1개 관련 문서 검색)"""
        retrieved_k = set(retrieved[:k])
        relevant_set = set(relevant)

        return 1.0 if retrieved_k & relevant_set else 0.0


# 사용
metrics = RetrievalMetrics()

# 검색 결과와 정답
retrieved = ["doc1", "doc3", "doc5", "doc2", "doc7"]
relevant = ["doc1", "doc2", "doc4"]

print(f"Precision@3: {metrics.precision_at_k(retrieved, relevant, 3):.2f}")
print(f"Recall@3: {metrics.recall_at_k(retrieved, relevant, 3):.2f}")
print(f"F1@3: {metrics.f1_at_k(retrieved, relevant, 3):.2f}")
print(f"MRR: {metrics.mrr(retrieved, relevant):.2f}")
print(f"Hit Rate@5: {metrics.hit_rate(retrieved, relevant, 5):.2f}")
