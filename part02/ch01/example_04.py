# 텍스트로 검색
results = collection.query(
    query_texts=["프로그래밍 배우기"],
    n_results=5
)

# 결과 구조
print(results["ids"])        # [['id1', 'id2', ...]]
print(results["documents"])  # [['문서1', '문서2', ...]]
print(results["distances"])  # [[0.12, 0.34, ...]]

# 결과 사용
for i, doc in enumerate(results["documents"][0]):
    distance = results["distances"][0][i]
    print(f"[{distance:.3f}] {doc[:50]}...")
