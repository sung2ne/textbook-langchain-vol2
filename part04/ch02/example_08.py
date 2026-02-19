from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from typing import List


class AdvancedHybridSearch:
    """고급 하이브리드 검색 시스템"""

    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

        # 벡터 저장소
        self.vectorstore = Chroma.from_documents(documents, self.embeddings)

        # BM25
        self.bm25_retriever = BM25Retriever.from_documents(documents)

    def search(self, query: str, k: int = 5,
               method: str = "ensemble",
               bm25_weight: float = 0.5) -> List[Document]:
        """검색 실행"""
        if method == "bm25":
            self.bm25_retriever.k = k
            return self.bm25_retriever.invoke(query)

        elif method == "vector":
            return self.vectorstore.similarity_search(query, k=k)

        elif method == "ensemble":
            self.bm25_retriever.k = k
            vector_retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": k}
            )

            ensemble = EnsembleRetriever(
                retrievers=[self.bm25_retriever, vector_retriever],
                weights=[bm25_weight, 1 - bm25_weight]
            )
            return ensemble.invoke(query)

        elif method == "rrf":
            self.bm25_retriever.k = k * 2
            bm25_results = self.bm25_retriever.invoke(query)
            vector_results = self.vectorstore.similarity_search(query, k=k * 2)
            return reciprocal_rank_fusion([bm25_results, vector_results])[:k]

        return []

    def compare_methods(self, query: str, k: int = 3):
        """검색 방식 비교"""
        methods = ["bm25", "vector", "ensemble", "rrf"]

        print(f"쿼리: {query}\n")

        for method in methods:
            print(f"=== {method.upper()} ===")
            results = self.search(query, k=k, method=method)

            for i, doc in enumerate(results, 1):
                print(f"  {i}. {doc.page_content[:50]}...")

            print()


# 사용
documents = [
    Document(page_content="Python은 1991년에 만들어진 프로그래밍 언어입니다."),
    Document(page_content="파이썬으로 웹 애플리케이션을 개발할 수 있습니다."),
    Document(page_content="LangChain은 LLM 애플리케이션 프레임워크입니다."),
    Document(page_content="RAG는 검색 증강 생성으로, 외부 지식을 활용합니다."),
    Document(page_content="벡터 데이터베이스는 임베딩을 저장하고 검색합니다."),
    Document(page_content="ChromaDB는 사용하기 쉬운 벡터 DB입니다."),
]

search_system = AdvancedHybridSearch(documents)

# 비교
search_system.compare_methods("파이썬 프로그래밍")
search_system.compare_methods("LLM 개발 도구")
