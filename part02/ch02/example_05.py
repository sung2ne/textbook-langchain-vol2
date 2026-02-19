# 기본 검색
results = vectorstore.similarity_search("AI 개발 도구", k=3)

for doc in results:
    print(f"내용: {doc.page_content[:50]}...")
    print(f"메타: {doc.metadata}")
    print()
