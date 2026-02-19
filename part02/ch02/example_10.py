# 나중에 다시 로드
vectorstore = Chroma(
    collection_name="persistent_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db"
)

# 기존 데이터로 검색
results = vectorstore.similarity_search("문서")
print(f"검색 결과: {len(results)}개")
