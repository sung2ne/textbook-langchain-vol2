from langchain_pinecone import PineconeVectorStore
from langchain_ollama import OllamaEmbeddings
import os

os.environ["PINECONE_API_KEY"] = "your_api_key"

embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 인덱스에 연결
vectorstore = PineconeVectorStore(
    index_name="my-index",
    embedding=embeddings
)

# 문서 추가
vectorstore.add_texts(["새 문서"])

# 검색
results = vectorstore.similarity_search("검색어")
