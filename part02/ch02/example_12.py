# 기본 Retriever
retriever = vectorstore.as_retriever()

# 검색 매개변수 설정
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# MMR (Maximal Marginal Relevance) - 다양성 고려
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20,  # 후보 수
        "lambda_mult": 0.5  # 다양성 가중치
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

# 사용
docs = retriever.invoke("검색 질문")
for doc in docs:
    print(doc.page_content[:50])
