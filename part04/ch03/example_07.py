def rerank_with_threshold(reranker, query: str, documents: List[Document],
                           top_k: int = 5, threshold: float = 0.3):
    """임계값 필터링 리랭킹"""
    reranked = reranker.rerank(query, documents, top_k=len(documents))

    # 임계값 이상만 반환
    filtered = [(doc, score) for doc, score in reranked if score >= threshold]

    return filtered[:top_k]


# 사용
results = rerank_with_threshold(reranker, query, documents, top_k=3, threshold=0.5)

if not results:
    print("관련 문서를 찾을 수 없습니다.")
else:
    for doc, score in results:
        print(f"[{score:.4f}] {doc.page_content}")
