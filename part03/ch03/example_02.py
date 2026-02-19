from abc import ABC, abstractmethod


class BaseRetriever(ABC):
    @abstractmethod
    def invoke(self, query: str) -> List[Document]:
        """질문에 관련된 문서 반환"""
        pass
