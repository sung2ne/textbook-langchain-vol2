# 어느 문서에서 정보를 가져왔는지 알 수 있음
results = vectorstore.similarity_search_with_score(query)
for doc, score in results:
    print(f"출처: {doc.metadata['source']}, 유사도: {score}")
