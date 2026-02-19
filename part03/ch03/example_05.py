# 유사도 검색 (기본)
retriever = vectorstore.as_retriever(
    search_type="similarity"
)

# MMR (다양성 고려)
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20,      # 후보 수
        "lambda_mult": 0.5  # 다양성 (0=다양, 1=유사)
    }
)

# 점수 임계값
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "score_threshold": 0.5,  # 최소 유사도
        "k": 10
    }
)
