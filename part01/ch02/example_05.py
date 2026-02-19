def find_similar_with_threshold(query, documents, embeddings,
                                 threshold=0.5, top_k=3):
    """임계값 이상인 유사 문서만 반환"""
    results = find_similar(query, documents, embeddings, top_k=len(documents))

    # 임계값 필터링
    filtered = [(idx, sim, doc) for idx, sim, doc in results if sim >= threshold]

    return filtered[:top_k]


# 사용
results = find_similar_with_threshold(
    "맛있는 음식",
    documents,
    embeddings,
    threshold=0.5
)

if not results:
    print("관련 문서를 찾을 수 없습니다.")
else:
    for idx, sim, doc in results:
        print(f"[{sim:.3f}] {doc}")
