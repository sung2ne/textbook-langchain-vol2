from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 텍스트를 벡터로 변환
vector = embeddings.embed_query("LangChain은 LLM 애플리케이션 프레임워크입니다.")

print(f"벡터 차원: {len(vector)}")  # 768
print(f"벡터 일부: {vector[:5]}")   # [0.123, -0.456, 0.789, ...]
