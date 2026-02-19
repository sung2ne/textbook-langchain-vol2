def find_similar(query, documents, embeddings, top_k=3):
    """가장 유사한 문서 찾기"""
    # 질문 임베딩
    query_vector = embeddings.embed_query(query)

    # 문서 임베딩
    doc_vectors = embeddings.embed_documents(documents)

    # 유사도 계산
    similarities = []
    for i, doc_vec in enumerate(doc_vectors):
        sim = cosine_similarity(query_vector, doc_vec)
        similarities.append((i, sim, documents[i]))

    # 유사도 순 정렬
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:top_k]


# 사용
documents = [
    "파이썬은 프로그래밍 언어입니다.",
    "LangChain은 LLM 애플리케이션 프레임워크입니다.",
    "벡터 데이터베이스는 임베딩을 저장합니다.",
    "오늘 점심은 김치찌개입니다.",
    "RAG는 검색 증강 생성 기술입니다.",
]

query = "LLM 앱을 만드는 방법"
results = find_similar(query, documents, embeddings, top_k=3)

print(f"질문: {query}\n")
print("유사한 문서:")
for idx, sim, doc in results:
    print(f"  [{sim:.3f}] {doc}")
