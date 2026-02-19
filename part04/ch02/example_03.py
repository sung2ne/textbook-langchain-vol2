# 키워드 중심 (기술 문서, API 문서)
ensemble_keyword_focused = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.7, 0.3]
)

# 의미 중심 (자연어, 설명 문서)
ensemble_semantic_focused = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.3, 0.7]
)

# 균형
ensemble_balanced = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.5, 0.5]
)
