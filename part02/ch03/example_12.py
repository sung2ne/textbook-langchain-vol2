# 기본 Retriever
retriever = vectorstore.as_retriever()

# 검색 설정
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# MMR (다양성 고려)
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20,
        "lambda_mult": 0.5
    }
)

# 사용
docs = retriever.invoke("검색어")
