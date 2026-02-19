def test_embedding_quality(embeddings, test_cases):
    """임베딩 품질 테스트

    test_cases: [
        {"query": "질문", "positive": "유사 문서", "negative": "비유사 문서"},
        ...
    ]
    """
    passed = 0
    failed = 0

    for tc in test_cases:
        query_vec = embeddings.embed_query(tc["query"])
        pos_vec = embeddings.embed_query(tc["positive"])
        neg_vec = embeddings.embed_query(tc["negative"])

        pos_sim = cosine_similarity(query_vec, pos_vec)
        neg_sim = cosine_similarity(query_vec, neg_vec)

        if pos_sim > neg_sim:
            passed += 1
            status = "✅"
        else:
            failed += 1
            status = "❌"

        print(f"{status} {tc['query'][:20]}...")
        print(f"   positive: {pos_sim:.3f}, negative: {neg_sim:.3f}")

    print(f"\n결과: {passed}/{len(test_cases)} 통과")
    return passed / len(test_cases)


# 테스트 케이스
test_cases = [
    {
        "query": "파이썬 프로그래밍",
        "positive": "Python 코딩 배우기",
        "negative": "오늘 점심 메뉴"
    },
    {
        "query": "LangChain RAG",
        "positive": "검색 증강 생성 프레임워크",
        "negative": "날씨가 좋습니다"
    },
]

score = test_embedding_quality(embeddings, test_cases)
print(f"품질 점수: {score:.1%}")
