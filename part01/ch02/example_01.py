import numpy as np


def cosine_similarity(vec1, vec2):
    """코사인 유사도 계산"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    return dot_product / (norm1 * norm2)


# 테스트
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

texts = [
    "오늘 날씨가 좋습니다.",
    "화창한 하루입니다.",
    "LangChain을 배웁니다.",
]

vectors = embeddings.embed_documents(texts)

# 유사도 계산
sim_01 = cosine_similarity(vectors[0], vectors[1])
sim_02 = cosine_similarity(vectors[0], vectors[2])

print(f"'{texts[0]}' vs '{texts[1]}': {sim_01:.4f}")
print(f"'{texts[0]}' vs '{texts[2]}': {sim_02:.4f}")
