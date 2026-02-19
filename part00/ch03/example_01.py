# 임베딩 확인
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector = embeddings.embed_query("테스트")
print(f"벡터 차원: {len(vector)}")  # 768
