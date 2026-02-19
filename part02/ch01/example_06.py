# 문서 업데이트
collection.update(
    ids=["doc1"],
    documents=["수정된 문서 내용"],
    metadatas=[{"updated": True}]
)

# 문서 삭제
collection.delete(ids=["doc1", "doc2"])

# 조건으로 삭제
collection.delete(where={"category": "old"})

# 문서 가져오기
docs = collection.get(ids=["doc1", "doc2"])
print(docs)

# 전체 문서 가져오기
all_docs = collection.get()
print(f"총 {len(all_docs['ids'])}개 문서")
