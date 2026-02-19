from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# 임베딩 모델
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 빈 벡터 저장소 생성
vectorstore = Chroma(
    collection_name="my_docs",
    embedding_function=embeddings
)
