from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# 임베딩
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 벡터 검색기
vectorstore = Chroma.from_documents(documents, embeddings)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# BM25 검색기
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 3

# 앙상블 검색기
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.5, 0.5]  # BM25 50%, Vector 50%
)

# 검색
results = ensemble_retriever.invoke("파이썬 프로그래밍 언어")

print("=== 앙상블 검색 결과 ===")
for doc in results:
    print(f"- {doc.page_content}")
