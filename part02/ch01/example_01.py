import chromadb

# 클라이언트 생성 (메모리 모드)
client = chromadb.Client()

# 컬렉션 생성
collection = client.create_collection("my_collection")

# 데이터 추가
collection.add(
    documents=["문서 1의 내용", "문서 2의 내용", "문서 3의 내용"],
    ids=["doc1", "doc2", "doc3"]
)

# 검색
results = collection.query(
    query_texts=["찾고 싶은 내용"],
    n_results=2
)

print(results)
