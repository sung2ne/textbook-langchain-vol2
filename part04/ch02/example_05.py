def reciprocal_rank_fusion(results_list: List[List[Document]],
                           k: int = 60) -> List[Document]:
    """RRF로 검색 결과 결합

    Args:
        results_list: 여러 검색기의 결과 리스트
        k: RRF 상수 (기본 60)
    """
    doc_scores = {}
    doc_objects = {}

    for results in results_list:
        for rank, doc in enumerate(results):
            key = doc.page_content

            # RRF 점수: 1 / (k + rank)
            score = 1 / (k + rank + 1)
            doc_scores[key] = doc_scores.get(key, 0) + score
            doc_objects[key] = doc

    # 점수순 정렬
    sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

    return [doc_objects[content] for content, score in sorted_docs]


# 사용
bm25_results = bm25_retriever.invoke("검색어")
vector_results = vector_retriever.invoke("검색어")

combined = reciprocal_rank_fusion([bm25_results, vector_results])

for doc in combined[:5]:
    print(f"- {doc.page_content}")
