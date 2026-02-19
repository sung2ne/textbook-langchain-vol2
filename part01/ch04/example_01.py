from abc import ABC, abstractmethod


class Embeddings(ABC):
    """LangChain 임베딩 기본 인터페이스"""

    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """여러 문서를 임베딩"""
        pass

    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        """단일 질문을 임베딩"""
        pass
