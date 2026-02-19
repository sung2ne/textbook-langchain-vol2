# app/services/embedding_service.py
from typing import List, Optional
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from app.config import settings
import os


class EmbeddingService:
    """임베딩 서비스"""

    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=settings.embedding_model
        )
        self._vectorstore: Optional[Chroma] = None

    @property
    def vectorstore(self) -> Optional[Chroma]:
        """벡터 저장소 (지연 로딩)"""
        if self._vectorstore is None:
            persist_dir = str(settings.vectorstore_dir)

            if os.path.exists(persist_dir) and os.listdir(persist_dir):
                self._vectorstore = Chroma(
                    persist_directory=persist_dir,
                    embedding_function=self.embeddings
                )

        return self._vectorstore

    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """벡터 저장소 생성"""
        persist_dir = str(settings.vectorstore_dir)

        self._vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=persist_dir
        )

        return self._vectorstore

    def add_documents(self, documents: List[Document]) -> int:
        """문서 추가"""
        if self._vectorstore is None:
            self.create_vectorstore(documents)
            return len(documents)

        self._vectorstore.add_documents(documents)
        return len(documents)

    def search(self, query: str, k: int = 5) -> List[Document]:
        """유사 문서 검색"""
        if self.vectorstore is None:
            return []

        return self.vectorstore.similarity_search(query, k=k)

    def search_with_score(self, query: str, k: int = 5
                         ) -> List[tuple[Document, float]]:
        """점수와 함께 검색"""
        if self.vectorstore is None:
            return []

        return self.vectorstore.similarity_search_with_score(query, k=k)

    def delete_by_source(self, source: str) -> int:
        """소스별 삭제"""
        if self.vectorstore is None:
            return 0

        # 메타데이터로 필터링하여 삭제
        results = self.vectorstore.get(
            where={"source": source}
        )

        if results and results.get("ids"):
            self.vectorstore.delete(ids=results["ids"])
            return len(results["ids"])

        return 0

    def get_stats(self) -> dict:
        """통계 반환"""
        if self.vectorstore is None:
            return {"chunk_count": 0, "sources": []}

        # 컬렉션 정보
        collection = self.vectorstore._collection
        count = collection.count()

        # 소스 목록 (샘플링)
        results = collection.peek(limit=100)
        sources = set()

        if results and results.get("metadatas"):
            for meta in results["metadatas"]:
                if meta and "source" in meta:
                    sources.add(meta["source"])

        return {
            "chunk_count": count,
            "sources": list(sources)
        }

    def reset(self):
        """벡터 저장소 초기화"""
        import shutil

        persist_dir = str(settings.vectorstore_dir)

        if os.path.exists(persist_dir):
            shutil.rmtree(persist_dir)

        self._vectorstore = None
        settings.vectorstore_dir.mkdir(exist_ok=True)
