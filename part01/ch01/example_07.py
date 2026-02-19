import numpy as np

texts = [
    "안녕하세요",
    "반갑습니다",
    "오늘 날씨가 좋네요",
    "LangChain 배우기",
]

vectors = embeddings.embed_documents(texts)

for i, (text, vec) in enumerate(zip(texts, vectors)):
    vec_np = np.array(vec)
    print(f"{i+1}. '{text}'")
    print(f"   평균: {vec_np.mean():.4f}, 표준편차: {vec_np.std():.4f}")
    print(f"   최소: {vec_np.min():.4f}, 최대: {vec_np.max():.4f}")
