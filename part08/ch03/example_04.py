# app/services/rag_service.py
from typing import List, Generator, Optional
from dataclasses import dataclass
from langchain_core.documents import Document
from app.config import settings
from app.services.embedding_service import EmbeddingService
from app.services.chunking_service import SmartChunker
from app.services.chain_service import ChainService
from app.models.schemas import QueryResponse, Source, SearchResult
import time


@dataclass
class RAGResult:
    """RAG 결과"""
    answer: str
    sources: List[Source]
    latency_ms: float


class RAGService:
    """통합 RAG 서비스"""

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.chunker = SmartChunker()
        self.chain_service = ChainService()

    def add_document(self, content: str, source: str,
                    doc_type: str = "text") -> int:
        """문서 추가"""
        # 청킹
        metadata = {"source": source}
        chunks = self.chunker.chunk(content, doc_type, metadata)

        # 임베딩 및 저장
        return self.embedding_service.add_documents(chunks)

    def query(self, question: str, k: int = None) -> QueryResponse:
        """질의응답"""
        k = k or settings.top_k
        start_time = time.time()

        # 검색
        results = self.embedding_service.search_with_score(question, k)

        if not results:
            return QueryResponse(
                answer="등록된 문서가 없습니다.",
                sources=[],
                latency_ms=(time.time() - start_time) * 1000
            )

        # 문서와 소스 분리
        documents = [doc for doc, _ in results]
        sources = [
            Source(
                content=doc.page_content[:200],
                source=doc.metadata.get("source", "unknown"),
                page=doc.metadata.get("page"),
                score=float(score)
            )
            for doc, score in results
        ]

        # 답변 생성
        answer = self.chain_service.answer(question, documents)

        return QueryResponse(
            answer=answer,
            sources=sources,
            latency_ms=(time.time() - start_time) * 1000
        )

    def stream_query(self, question: str,
                    k: int = None) -> Generator[dict, None, None]:
        """스트리밍 질의응답"""
        k = k or settings.top_k

        # 검색
        results = self.embedding_service.search_with_score(question, k)

        if not results:
            yield {"type": "error", "data": "등록된 문서가 없습니다."}
            return

        documents = [doc for doc, _ in results]

        # 소스 전송
        sources = [
            {
                "content": doc.page_content[:200],
                "source": doc.metadata.get("source", "unknown"),
                "score": float(score)
            }
            for doc, score in results
        ]
        yield {"type": "sources", "data": sources}

        # 답변 스트리밍
        for chunk in self.chain_service.stream_answer(question, documents):
            yield {"type": "token", "data": chunk}

        yield {"type": "done"}

    def search(self, query: str, k: int = 10) -> List[SearchResult]:
        """검색만 수행"""
        results = self.embedding_service.search_with_score(query, k)

        return [
            SearchResult(
                content=doc.page_content,
                source=doc.metadata.get("source", "unknown"),
                score=float(score),
                metadata=doc.metadata
            )
            for doc, score in results
        ]

    def delete_document(self, source: str) -> int:
        """문서 삭제"""
        return self.embedding_service.delete_by_source(source)

    def get_stats(self) -> dict:
        """통계"""
        return self.embedding_service.get_stats()

    def reset(self):
        """초기화"""
        self.embedding_service.reset()
