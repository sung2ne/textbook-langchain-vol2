from sentence_transformers import CrossEncoder
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.documents import Document
from typing import List, Tuple


class AdvancedRetrievalSystem:
    """고급 검색 시스템 (하이브리드 + 리랭킹)"""

    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

        # 벡터 저장소
        self.vectorstore = Chroma.from_documents(documents, self.embeddings)

        # BM25
        self.bm25_retriever = BM25Retriever.from_documents(documents)

        # 리랭커
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def retrieve(self, query: str, initial_k: int = 20, final_k: int = 5,
                 use_hybrid: bool = True, use_rerank: bool = True,
                 threshold: float = 0.0) -> List[Tuple[Document, float]]:
        """검색 실행"""
        # 1단계: 초기 검색
        if use_hybrid:
            self.bm25_retriever.k = initial_k
            vector_retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": initial_k}
            )

            ensemble = EnsembleRetriever(
                retrievers=[self.bm25_retriever, vector_retriever],
                weights=[0.4, 0.6]
            )
            initial_results = ensemble.invoke(query)
        else:
            initial_results = self.vectorstore.similarity_search(query, k=initial_k)

        if not initial_results:
            return []

        # 2단계: 리랭킹
        if use_rerank:
            pairs = [[query, doc.page_content] for doc in initial_results]
            scores = self.reranker.predict(pairs)

            doc_scores = list(zip(initial_results, scores))
            doc_scores.sort(key=lambda x: x[1], reverse=True)

            # 임계값 필터링
            filtered = [(doc, score) for doc, score in doc_scores if score >= threshold]
            return filtered[:final_k]
        else:
            return [(doc, 1.0) for doc in initial_results[:final_k]]

    def compare_settings(self, query: str):
        """다양한 설정 비교"""
        settings = [
            ("Vector만", {"use_hybrid": False, "use_rerank": False}),
            ("Vector + Rerank", {"use_hybrid": False, "use_rerank": True}),
            ("Hybrid만", {"use_hybrid": True, "use_rerank": False}),
            ("Hybrid + Rerank", {"use_hybrid": True, "use_rerank": True}),
        ]

        print(f"쿼리: {query}\n")

        for name, kwargs in settings:
            print(f"=== {name} ===")
            results = self.retrieve(query, **kwargs)

            for i, (doc, score) in enumerate(results[:3], 1):
                print(f"  {i}. [{score:.4f}] {doc.page_content[:40]}...")

            print()


# 테스트
documents = [
    Document(page_content="Python은 1991년에 만들어진 프로그래밍 언어입니다."),
    Document(page_content="파이썬은 간결한 문법이 특징입니다."),
    Document(page_content="LangChain은 LLM 앱 개발 프레임워크입니다."),
    Document(page_content="RAG는 검색 증강 생성 기술입니다."),
    Document(page_content="임베딩은 텍스트를 벡터로 변환합니다."),
    Document(page_content="벡터 DB는 유사도 검색에 특화되어 있습니다."),
    Document(page_content="파이썬으로 AI 애플리케이션을 개발합니다."),
    Document(page_content="오늘 날씨가 좋습니다."),
]

system = AdvancedRetrievalSystem(documents)

# 비교
system.compare_settings("파이썬 프로그래밍 언어")
system.compare_settings("AI 개발 도구")
