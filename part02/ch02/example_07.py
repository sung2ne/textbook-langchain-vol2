# 관련도 점수 (0~1, 높을수록 유사)
results = vectorstore.similarity_search_with_relevance_scores("LLM 앱", k=3)

for doc, score in results:
    print(f"[{score:.2%}] {doc.page_content[:50]}...")
