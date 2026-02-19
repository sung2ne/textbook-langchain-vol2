from langchain_ollama import OllamaEmbeddings

# 임베딩 생성
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector = embeddings.embed_query("검색할 텍스트")
