from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# BM25 (키워드 검색)
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 3

# 벡터 검색
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 앙상블 (하이브리드 검색)
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6]  # BM25 40%, 벡터 60%
)

results = ensemble_retriever.invoke("LangChain 튜토리얼")
