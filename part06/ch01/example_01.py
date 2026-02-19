import numpy as np


def dcg(relevances: list, k: int = None) -> float:
    """DCG 계산"""
    if k:
        relevances = relevances[:k]

    result = 0.0
    for i, rel in enumerate(relevances):
        # log2(i + 2): 순위가 낮을수록 할인
        result += rel / np.log2(i + 2)

    return result


def ndcg(relevances: list, k: int = None) -> float:
    """NDCG 계산"""
    # 이상적인 순서 (내림차순)
    ideal = sorted(relevances, reverse=True)

    dcg_val = dcg(relevances, k)
    idcg_val = dcg(ideal, k)

    if idcg_val == 0:
        return 0.0

    return dcg_val / idcg_val


# 사용 예시
# 관련도: 3=매우관련, 2=관련, 1=약간관련, 0=무관
relevances = [3, 2, 0, 1, 0]  # 검색 결과 순서대로

print(f"NDCG@5: {ndcg(relevances, 5):.3f}")
print(f"NDCG@3: {ndcg(relevances, 3):.3f}")
