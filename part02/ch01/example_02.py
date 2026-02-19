import chromadb

client = chromadb.Client()

# 컬렉션 생성
collection = client.create_collection("documents")

# 컬렉션 가져오기 (있으면 가져오고, 없으면 생성)
collection = client.get_or_create_collection("documents")

# 컬렉션 목록
collections = client.list_collections()
for col in collections:
    print(f"- {col.name}")

# 컬렉션 삭제
client.delete_collection("documents")
