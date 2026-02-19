import faiss
import numpy as np

# 벡터 차원
dimension = 768

# 인덱스 생성 (L2 거리)
index = faiss.IndexFlatL2(dimension)

# 벡터 추가
vectors = np.random.random((1000, dimension)).astype('float32')
index.add(vectors)

print(f"인덱스에 저장된 벡터 수: {index.ntotal}")

# 검색
query = np.random.random((1, dimension)).astype('float32')
k = 5  # 상위 5개

distances, indices = index.search(query, k)

print(f"가장 유사한 인덱스: {indices[0]}")
print(f"거리: {distances[0]}")
