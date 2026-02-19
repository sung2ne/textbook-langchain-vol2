# 평가 예시
def precision_at_k(retrieved, relevant, k):
    top_k = retrieved[:k]
    hits = sum(1 for doc in top_k if doc in relevant)
    return hits / k
