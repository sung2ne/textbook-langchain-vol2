from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings


def filtered_search(vectorstore, query: str, filters: dict, k: int = 5):
    """메타데이터 필터 검색"""
    results = vectorstore.similarity_search(
        query,
        k=k,
        filter=filters
    )
    return results


# 다양한 필터 예시
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(docs, embeddings)

# 특정 섹션 레벨만
results = filtered_search(vectorstore, "설치", {"level": 2})

# 범위 조건
results = filtered_search(vectorstore, "설치", {"level": {"$gte": 2}})

# 복합 조건
results = filtered_search(
    vectorstore,
    "설치",
    {
        "$and": [
            {"level": {"$gte": 1}},
            {"level": {"$lte": 3}}
        ]
    }
)
