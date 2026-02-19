# Qdrant - 안정적인 서버 모드
vectorstore = Qdrant.from_documents(
    documents,
    embeddings,
    url="http://localhost:6333",
    collection_name="production"
)
