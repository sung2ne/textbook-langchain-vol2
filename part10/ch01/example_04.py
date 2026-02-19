# 하이브리드 검색
from langchain.retrievers import EnsembleRetriever

hybrid = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.7, 0.3]
)
