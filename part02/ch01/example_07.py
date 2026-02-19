import chromadb

# 영속적 클라이언트
client = chromadb.PersistentClient(path="./chroma_db")

# 컬렉션 생성 및 데이터 추가
collection = client.get_or_create_collection("persistent_docs")
collection.add(
    documents=["저장될 문서"],
    ids=["saved_doc"]
)

# 프로그램 재시작 후에도 데이터 유지
