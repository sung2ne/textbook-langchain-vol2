from langchain_ollama import OllamaEmbeddings

# nomic-embed-text (768 차원)
embeddings_nomic = OllamaEmbeddings(model="nomic-embed-text")

# mxbai-embed-large (1024 차원)
embeddings_mxbai = OllamaEmbeddings(model="mxbai-embed-large")

# 테스트
text = "LangChain은 LLM 프레임워크입니다."

vec1 = embeddings_nomic.embed_query(text)
vec2 = embeddings_mxbai.embed_query(text)

print(f"nomic 차원: {len(vec1)}")   # 768
print(f"mxbai 차원: {len(vec2)}")   # 1024
