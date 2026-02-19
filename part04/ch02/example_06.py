def normalize_scores(results_with_scores: List[tuple]) -> List[tuple]:
    """점수 정규화 (0-1 범위)"""
    if not results_with_scores:
        return []

    scores = [score for doc, score in results_with_scores]
    min_score = min(scores)
    max_score = max(scores)

    if max_score == min_score:
        return [(doc, 1.0) for doc, score in results_with_scores]

    normalized = [
        (doc, (score - min_score) / (max_score - min_score))
        for doc, score in results_with_scores
    ]

    return normalized


def hybrid_search_with_scores(query: str, vectorstore, bm25_docs,
                               bm25_weight: float = 0.5) -> List[Document]:
    """점수 기반 하이브리드 검색"""
    # 벡터 검색 (점수 포함)
    vector_results = vectorstore.similarity_search_with_relevance_scores(query, k=10)
    vector_normalized = normalize_scores(vector_results)

    # BM25 검색 (점수 계산)
    bm25_retriever = BM25Retriever.from_documents(bm25_docs)
    bm25_retriever.k = 10
    bm25_results = bm25_retriever.invoke(query)

    # BM25는 순위 기반 점수
    bm25_with_scores = [(doc, 1 / (i + 1)) for i, doc in enumerate(bm25_results)]
    bm25_normalized = normalize_scores(bm25_with_scores)

    # 결합
    combined_scores = {}
    all_docs = {}

    for doc, score in vector_normalized:
        key = doc.page_content
        combined_scores[key] = (1 - bm25_weight) * score
        all_docs[key] = doc

    for doc, score in bm25_normalized:
        key = doc.page_content
        combined_scores[key] = combined_scores.get(key, 0) + bm25_weight * score
        all_docs[key] = doc

    # 정렬
    sorted_keys = sorted(combined_scores.keys(),
                         key=lambda x: combined_scores[x],
                         reverse=True)

    return [all_docs[key] for key in sorted_keys]
