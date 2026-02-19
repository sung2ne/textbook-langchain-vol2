from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from typing import List


class RetrieveAndRerank:
    """검색 + 리랭킹 파이프라인"""

    def __init__(self, documents: List[Document], reranker=None):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vectorstore = Chroma.from_documents(documents, self.embeddings)
        self.reranker = reranker or CrossEncoderReranker()

    def retrieve(self, query: str, initial_k: int = 20, final_k: int = 5):
        """검색 및 리랭킹"""
        # 1단계: 초기 검색 (많이 가져옴)
        initial_results = self.vectorstore.similarity_search(query, k=initial_k)

        # 2단계: 리랭킹 (상위 선별)
        reranked = self.reranker.rerank(query, initial_results, top_k=final_k)

        return reranked


# 사용
pipeline = RetrieveAndRerank(documents)

results = pipeline.retrieve("Python AI 개발", initial_k=10, final_k=3)

for doc, score in results:
    print(f"[{score:.4f}] {doc.page_content}")
