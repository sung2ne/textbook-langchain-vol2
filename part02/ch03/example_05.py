# HNSW - 빠르고 정확한 근사 검색
M = 32  # 연결 수

index = faiss.IndexHNSWFlat(dimension, M)
index.add(vectors)

# 검색
distances, indices = index.search(query, k)
