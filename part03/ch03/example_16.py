from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from typing import List


class AdvancedRetrieverSystem:
    """고급 검색 시스템"""

    def __init__(self, documents: List[Document]):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vectorstore = Chroma.from_documents(documents, self.embeddings)

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """기본 유사도 검색"""
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
        return retriever.invoke(query)

    def mmr_search(self, query: str, k: int = 5, diversity: float = 0.5) -> List[Document]:
        """다양성 고려 검색"""
        retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": k,
                "fetch_k": k * 4,
                "lambda_mult": 1 - diversity
            }
        )
        return retriever.invoke(query)

    def filtered_search(self, query: str, filter_dict: dict, k: int = 5) -> List[Document]:
        """필터 검색"""
        retriever = self.vectorstore.as_retriever(
            search_kwargs={
                "k": k,
                "filter": filter_dict
            }
        )
        return retriever.invoke(query)

    def threshold_search(self, query: str, threshold: float = 0.5) -> List[Document]:
        """임계값 검색"""
        results = self.vectorstore.similarity_search_with_relevance_scores(
            query, k=20
        )
        return [doc for doc, score in results if score >= threshold]


# 사용
documents = [
    Document(page_content="파이썬 기초 문법", metadata={"level": "beginner"}),
    Document(page_content="파이썬 고급 기법", metadata={"level": "advanced"}),
    Document(page_content="LangChain 시작하기", metadata={"level": "beginner"}),
    Document(page_content="RAG 아키텍처 설계", metadata={"level": "advanced"}),
]

system = AdvancedRetrieverSystem(documents)

# 다양한 검색
print("=== 기본 검색 ===")
for doc in system.similarity_search("프로그래밍", k=2):
    print(f"- {doc.page_content}")

print("\n=== MMR 검색 (다양성 높음) ===")
for doc in system.mmr_search("프로그래밍", k=2, diversity=0.8):
    print(f"- {doc.page_content}")

print("\n=== 필터 검색 (초급) ===")
for doc in system.filtered_search("개발", {"level": "beginner"}, k=2):
    print(f"- {doc.page_content}")
