# 클러스터 기반 근사 검색
nlist = 100  # 클러스터 수

quantizer = faiss.IndexFlatL2(dimension)
index = faiss.IndexIVFFlat(quantizer, dimension, nlist)

# 학습 필요
index.train(vectors)
index.add(vectors)

# 검색 시 탐색할 클러스터 수
index.nprobe = 10
distances, indices = index.search(query, k)
