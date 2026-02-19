# ChromaDB - 가장 쉬운 시작
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
