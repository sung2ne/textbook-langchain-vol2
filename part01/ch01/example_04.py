from langchain_ollama import OllamaEmbeddings

# 임베딩 모델 초기화
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 단일 텍스트 임베딩
text = "오늘 날씨가 좋습니다."
vector = embeddings.embed_query(text)

print(f"입력: {text}")
print(f"벡터 길이: {len(vector)}")
print(f"벡터 타입: {type(vector)}")
print(f"처음 5개 값: {vector[:5]}")
