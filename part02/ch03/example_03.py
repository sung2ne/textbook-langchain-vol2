# 내적 (코사인 유사도에 사용)
index = faiss.IndexFlatIP(dimension)

# 정규화된 벡터로 코사인 유사도
faiss.normalize_L2(vectors)
index.add(vectors)
