def analyze_query(query: str) -> dict:
    """쿼리 분석"""
    analysis = {
        "has_code_terms": False,
        "is_question": False,
        "word_count": len(query.split())
    }

    # 코드 관련 용어 확인
    code_terms = ["함수", "클래스", "메서드", "API", "function", "class", "method"]
    analysis["has_code_terms"] = any(term in query.lower() for term in code_terms)

    # 질문 여부
    analysis["is_question"] = query.endswith("?") or any(
        q in query for q in ["뭐", "어떻게", "왜", "언제", "무엇"]
    )

    return analysis


def dynamic_hybrid_retriever(query: str, bm25_retriever, vector_retriever) -> List[Document]:
    """동적 가중치 하이브리드 검색"""
    analysis = analyze_query(query)

    # 가중치 결정
    if analysis["has_code_terms"]:
        bm25_weight = 0.6  # 코드: 키워드 중심
    elif analysis["is_question"] and analysis["word_count"] > 5:
        bm25_weight = 0.3  # 긴 질문: 의미 중심
    else:
        bm25_weight = 0.5  # 균형

    print(f"쿼리 분석: {analysis}")
    print(f"BM25 가중치: {bm25_weight}")

    # 검색
    ensemble = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[bm25_weight, 1 - bm25_weight]
    )

    return ensemble.invoke(query)


# 테스트
queries = [
    "Python 함수 정의 방법",
    "왜 LangChain을 사용해야 하나요?",
    "RAG",
]

for q in queries:
    print(f"\n=== 쿼리: {q} ===")
    results = dynamic_hybrid_retriever(q, bm25_retriever, vector_retriever)
    for doc in results[:2]:
        print(f"- {doc.page_content[:50]}...")
