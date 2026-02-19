import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine


def similarity_matrix(texts, embeddings):
    """텍스트 간 유사도 행렬"""
    vectors = embeddings.embed_documents(texts)
    vectors_np = np.array(vectors)

    # sklearn으로 한번에 계산
    sim_matrix = sklearn_cosine(vectors_np)

    return sim_matrix


# 사용
texts = [
    "강아지가 뛰어다닌다",
    "개가 달리고 있다",
    "고양이가 잠을 잔다",
    "주식 시장이 상승했다",
]

matrix = similarity_matrix(texts, embeddings)

# 출력
print("유사도 행렬:")
print("          ", end="")
for i in range(len(texts)):
    print(f"[{i}]   ", end="")
print()

for i, text in enumerate(texts):
    print(f"[{i}] ", end="")
    for j in range(len(texts)):
        print(f"{matrix[i][j]:.2f}  ", end="")
    print(f"  {text[:10]}...")
