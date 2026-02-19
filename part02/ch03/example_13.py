from tqdm import tqdm


def create_faiss_index(documents, embeddings, batch_size=1000):
    """대규모 문서로 FAISS 인덱스 생성"""
    vectorstore = None

    for i in tqdm(range(0, len(documents), batch_size)):
        batch = documents[i:i + batch_size]

        if vectorstore is None:
            vectorstore = FAISS.from_documents(batch, embeddings)
        else:
            batch_store = FAISS.from_documents(batch, embeddings)
            vectorstore.merge_from(batch_store)

    return vectorstore


# 대량 문서 처리
documents = [Document(page_content=f"문서 {i}") for i in range(10000)]
vectorstore = create_faiss_index(documents, embeddings, batch_size=500)

print(f"총 벡터 수: {vectorstore.index.ntotal}")
