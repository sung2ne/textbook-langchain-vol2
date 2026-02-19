import time
from langchain_core.documents import Document


def benchmark_vectorstore(name, vectorstore, documents, queries):
    """벡터 저장소 벤치마크"""
    results = {"name": name}

    # 추가 시간
    start = time.time()
    vectorstore.add_documents(documents)
    results["add_time"] = time.time() - start

    # 검색 시간
    search_times = []
    for query in queries:
        start = time.time()
        vectorstore.similarity_search(query, k=5)
        search_times.append(time.time() - start)

    results["avg_search_time"] = sum(search_times) / len(search_times)
    results["total_docs"] = len(documents)

    return results


# 테스트 데이터
documents = [Document(page_content=f"테스트 문서 {i}") for i in range(1000)]
queries = ["검색어 1", "검색어 2", "검색어 3"]

# ChromaDB 벤치마크
from langchain_community.vectorstores import Chroma

chroma = Chroma(embedding_function=embeddings)
chroma_results = benchmark_vectorstore("ChromaDB", chroma, documents[:100], queries)

# FAISS 벤치마크
from langchain_community.vectorstores import FAISS

faiss_store = FAISS.from_documents(documents[:100], embeddings)
faiss_results = benchmark_vectorstore("FAISS", faiss_store, documents[100:200], queries)

# 결과 출력
for r in [chroma_results, faiss_results]:
    print(f"\n{r['name']}:")
    print(f"  추가 시간: {r['add_time']:.3f}초")
    print(f"  평균 검색 시간: {r['avg_search_time']*1000:.2f}ms")
