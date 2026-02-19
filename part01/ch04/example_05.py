from tqdm import tqdm


def embed_documents_batch(embeddings, documents, batch_size=100):
    """대량 문서를 배치로 임베딩"""
    all_vectors = []

    for i in tqdm(range(0, len(documents), batch_size)):
        batch = documents[i:i + batch_size]
        vectors = embeddings.embed_documents(batch)
        all_vectors.extend(vectors)

    return all_vectors


# 사용
documents = [f"문서 {i}의 내용입니다." for i in range(1000)]
embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectors = embed_documents_batch(embeddings, documents, batch_size=50)
print(f"총 {len(vectors)}개 벡터 생성")
