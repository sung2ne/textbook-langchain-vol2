class SimpleSearchEngine:
    def __init__(self, model="nomic-embed-text"):
        self.embeddings = OllamaEmbeddings(model=model)
        self.documents = []
        self.vectors = []

    def add_documents(self, docs):
        """문서 추가"""
        self.documents.extend(docs)
        vectors = self.embeddings.embed_documents(docs)
        self.vectors.extend(vectors)
        print(f"{len(docs)}개 문서 추가됨 (총 {len(self.documents)}개)")

    def search(self, query, top_k=3, threshold=0.0):
        """검색"""
        if not self.documents:
            return []

        query_vector = self.embeddings.embed_query(query)

        # 유사도 계산
        results = []
        for i, doc_vec in enumerate(self.vectors):
            sim = cosine_similarity(query_vector, doc_vec)
            if sim >= threshold:
                results.append({
                    "document": self.documents[i],
                    "similarity": sim,
                    "index": i
                })

        # 정렬
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]


# 사용
engine = SimpleSearchEngine()
engine.add_documents([
    "파이썬으로 웹 개발하기",
    "LangChain 튜토리얼",
    "머신러닝 기초",
    "FastAPI로 API 만들기",
    "벡터 데이터베이스 소개",
])

results = engine.search("AI 앱 개발")
for r in results:
    print(f"[{r['similarity']:.3f}] {r['document']}")
