# Chroma 확인
import chromadb

client = chromadb.Client()
collection = client.create_collection("test")
print("Chroma 정상 동작")
