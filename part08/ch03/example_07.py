# app/services/pipeline_service.py
from typing import List, Generator, Optional
from dataclasses import dataclass
from app.services.rag_service import RAGService
from app.services.loader_service import LoaderService
from app.services.cache_service import QueryCache
from app.models.schemas import QueryResponse
import logging

logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """파이프라인 설정"""
    use_cache: bool = True
    min_score: float = 0.0
    max_sources: int = 5
    stream: bool = False


class RAGPipeline:
    """RAG 파이프라인"""

    def __init__(self, config: PipelineConfig = None):
        self.config = config or PipelineConfig()
        self.rag_service = RAGService()
        self.loader_service = LoaderService()
        self.query_cache = QueryCache() if self.config.use_cache else None

    def ingest(self, file_path: str) -> dict:
        """문서 수집"""
        try:
            # 로드
            content, doc_type = self.loader_service.load(file_path)

            # RAG에 추가
            chunks = self.rag_service.add_document(
                content=content,
                source=file_path,
                doc_type=doc_type
            )

            logger.info(f"문서 수집 완료: {file_path} ({chunks} 청크)")

            return {
                "success": True,
                "source": file_path,
                "chunks": chunks
            }

        except Exception as e:
            logger.error(f"문서 수집 실패: {file_path} - {e}")
            return {
                "success": False,
                "source": file_path,
                "error": str(e)
            }

    def ingest_bytes(self, content: bytes, filename: str) -> dict:
        """바이트에서 문서 수집"""
        try:
            text, doc_type = self.loader_service.load_bytes(content, filename)

            chunks = self.rag_service.add_document(
                content=text,
                source=filename,
                doc_type=doc_type
            )

            return {
                "success": True,
                "source": filename,
                "chunks": chunks
            }

        except Exception as e:
            return {
                "success": False,
                "source": filename,
                "error": str(e)
            }

    def query(self, question: str, k: int = 5) -> QueryResponse:
        """질의"""
        # 캐시 확인
        if self.query_cache:
            cached = self.query_cache.get_cached_answer(question, k)
            if cached:
                logger.info(f"캐시 히트: {question[:30]}...")
                return QueryResponse(**cached)

        # RAG 실행
        response = self.rag_service.query(question, k)

        # 최소 점수 필터링
        if self.config.min_score > 0:
            response.sources = [
                s for s in response.sources
                if s.score >= self.config.min_score
            ]

        # 소스 수 제한
        response.sources = response.sources[:self.config.max_sources]

        # 캐시 저장
        if self.query_cache:
            self.query_cache.cache_answer(
                question, k,
                response.model_dump()
            )

        return response

    def stream_query(self, question: str,
                    k: int = 5) -> Generator[dict, None, None]:
        """스트리밍 질의"""
        yield from self.rag_service.stream_query(question, k)


class BatchPipeline:
    """배치 처리 파이프라인"""

    def __init__(self):
        self.pipeline = RAGPipeline()

    def ingest_directory(self, directory: str) -> List[dict]:
        """디렉토리 일괄 수집"""
        from pathlib import Path

        results = []
        path = Path(directory)

        for file_path in path.rglob("*"):
            if file_path.is_file():
                ext = file_path.suffix.lower()

                if ext in LoaderService.SUPPORTED_EXTENSIONS:
                    result = self.pipeline.ingest(str(file_path))
                    results.append(result)

        return results

    def batch_query(self, questions: List[str],
                   k: int = 5) -> List[QueryResponse]:
        """일괄 질의"""
        return [
            self.pipeline.query(q, k)
            for q in questions
        ]
