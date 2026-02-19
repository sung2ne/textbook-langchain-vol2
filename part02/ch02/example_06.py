# 유사도 점수 포함
results = vectorstore.similarity_search_with_score("프로그래밍 언어", k=3)

for doc, score in results:
    print(f"[{score:.4f}] {doc.page_content[:50]}...")
