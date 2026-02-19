# 대규모 데이터용 설정
vectorstore = Chroma(
    collection_name="large_docs",
    embedding_function=embeddings,
    collection_metadata={"hnsw:space": "cosine"}  # 거리 메트릭
)
