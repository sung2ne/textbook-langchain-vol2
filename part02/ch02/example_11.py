# 문서 추가
new_docs = [
    Document(page_content="새로운 문서 1", metadata={"new": True}),
    Document(page_content="새로운 문서 2", metadata={"new": True}),
]

ids = vectorstore.add_documents(new_docs)
print(f"추가된 ID: {ids}")

# 텍스트로 추가
ids = vectorstore.add_texts(
    texts=["텍스트로 추가"],
    metadatas=[{"method": "add_texts"}]
)

# 문서 삭제
vectorstore.delete(ids=ids)
print("삭제 완료")
