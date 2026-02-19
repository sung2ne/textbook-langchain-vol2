retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,           # 최종 반환 수
        "fetch_k": 20,    # 후보군 크기
        "lambda_mult": 0.5
    }
)

results = retriever.invoke("파이썬")
