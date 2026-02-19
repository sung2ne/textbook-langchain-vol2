from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.vectorstores import Chroma
import os

os.environ["COHERE_API_KEY"] = "your_api_key"

# 기본 retriever
vectorstore = Chroma.from_documents(documents, embeddings)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# Cohere 리랭커
compressor = CohereRerank(top_n=3)

# 압축 retriever (리랭킹 적용)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

# 검색 (리랭킹 포함)
results = compression_retriever.invoke("질문")
