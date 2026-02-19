# 나중에 다시 연결
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("persistent_docs")

# 기존 데이터 확인
results = collection.get()
print(f"저장된 문서: {len(results['ids'])}개")
