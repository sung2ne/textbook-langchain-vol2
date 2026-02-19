import chromadb


class DocumentSearch:
    def __init__(self, persist_dir="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection("documents")

    def add_documents(self, documents, ids=None, metadatas=None):
        """문서 추가"""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]

        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        print(f"{len(documents)}개 문서 추가됨")

    def search(self, query, n_results=5, where=None):
        """검색"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )

        # 결과 정리
        formatted = []
        for i, doc in enumerate(results["documents"][0]):
            formatted.append({
                "id": results["ids"][0][i],
                "document": doc,
                "distance": results["distances"][0][i],
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {}
            })

        return formatted

    def count(self):
        """문서 수"""
        return self.collection.count()


# 사용
search = DocumentSearch()

# 문서 추가
docs = [
    "파이썬은 배우기 쉬운 프로그래밍 언어입니다.",
    "LangChain은 LLM 애플리케이션 프레임워크입니다.",
    "RAG는 검색 증강 생성 기술입니다.",
    "벡터 데이터베이스는 임베딩을 저장합니다.",
    "ChromaDB는 사용하기 쉬운 벡터 DB입니다.",
]

search.add_documents(
    docs,
    metadatas=[{"topic": "python"}, {"topic": "langchain"}, {"topic": "rag"},
               {"topic": "vectordb"}, {"topic": "vectordb"}]
)

# 검색
print(f"\n총 {search.count()}개 문서")
print("\n검색: 'AI 개발'")

results = search.search("AI 개발", n_results=3)
for r in results:
    print(f"[{r['distance']:.3f}] {r['document'][:40]}...")

# 필터 검색
print("\n검색: 'vectordb' 토픽만")
results = search.search("데이터베이스", where={"topic": "vectordb"})
for r in results:
    print(f"[{r['distance']:.3f}] {r['document'][:40]}...")
