# 정확한 L2 거리 검색
index = faiss.IndexFlatL2(dimension)
index.add(vectors)

# 장점: 정확함
# 단점: 대규모에서 느림
