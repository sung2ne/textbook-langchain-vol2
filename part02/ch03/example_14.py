# GPU 사용 (faiss-gpu 설치 필요)
import faiss

# CPU 인덱스를 GPU로 이동
cpu_index = faiss.IndexFlatL2(dimension)
cpu_index.add(vectors)

# GPU 리소스
res = faiss.StandardGpuResources()

# GPU 인덱스로 변환
gpu_index = faiss.index_cpu_to_gpu(res, 0, cpu_index)

# GPU에서 검색 (훨씬 빠름)
distances, indices = gpu_index.search(query, k)
