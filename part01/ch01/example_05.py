texts = [
    "오늘 날씨가 좋습니다.",
    "화창한 하루입니다.",
    "비가 오고 있습니다.",
    "LangChain은 프레임워크입니다.",
]

# 여러 텍스트 한번에 임베딩
vectors = embeddings.embed_documents(texts)

print(f"텍스트 수: {len(texts)}")
print(f"벡터 수: {len(vectors)}")
print(f"각 벡터 차원: {len(vectors[0])}")
