# 첫 번째 벡터 저장소
texts1 = ["문서 1", "문서 2"]
vectorstore1 = FAISS.from_texts(texts1, embeddings)

# 두 번째 벡터 저장소
texts2 = ["문서 3", "문서 4"]
vectorstore2 = FAISS.from_texts(texts2, embeddings)

# 병합
vectorstore1.merge_from(vectorstore2)

print(f"병합 후 문서 수: {vectorstore1.index.ntotal}")
