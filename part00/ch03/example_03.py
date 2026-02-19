# FAISS 확인
import faiss
import numpy as np

index = faiss.IndexFlatL2(768)
print("FAISS 정상 동작")
