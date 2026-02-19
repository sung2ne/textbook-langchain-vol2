# 기본 검색
results = vectorstore.similarity_search("날씨 정보", k=3)

# 점수와 함께 검색
results = vectorstore.similarity_search_with_score("프로그래밍", k=3)
for doc, score in results:
    print(f"[{score:.4f}] {doc.page_content}")

# 관련도 점수
results = vectorstore.similarity_search_with_relevance_scores("개발", k=3)
for doc, score in results:
    print(f"[{score:.2%}] {doc.page_content}")
