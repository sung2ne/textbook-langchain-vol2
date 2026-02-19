# 저장
vectorstore.save_local("./faiss_index")

# 로드
loaded_vectorstore = FAISS.load_local(
    "./faiss_index",
    embeddings,
    allow_dangerous_deserialization=True  # pickle 사용
)

# 검색 테스트
results = loaded_vectorstore.similarity_search("테스트")
print(f"검색 결과: {len(results)}개")
