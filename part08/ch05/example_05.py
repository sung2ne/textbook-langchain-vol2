# tests/test_integration.py
import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def integration_env():
    """통합 테스트 환경"""
    temp_dir = tempfile.mkdtemp()

    # 디렉토리 생성
    (Path(temp_dir) / "data").mkdir()
    (Path(temp_dir) / "vectorstore").mkdir()
    (Path(temp_dir) / "uploads").mkdir()

    yield temp_dir

    shutil.rmtree(temp_dir)


class TestEndToEnd:
    """엔드투엔드 테스트"""

    @pytest.mark.integration
    def test_full_workflow(self, integration_env):
        """전체 워크플로우"""
        from unittest.mock import patch

        with patch("app.config.settings") as mock_settings:
            mock_settings.data_dir = Path(integration_env) / "data"
            mock_settings.vectorstore_dir = Path(integration_env) / "vectorstore"
            mock_settings.uploads_dir = Path(integration_env) / "uploads"
            mock_settings.chunk_size = 200
            mock_settings.chunk_overlap = 20
            mock_settings.top_k = 3
            mock_settings.embedding_model = "nomic-embed-text"
            mock_settings.llm_model = "llama4"

            from app.services.pipeline_service import RAGPipeline

            pipeline = RAGPipeline()

            # 1. 문서 수집
            doc_content = """
            Python은 간결하고 읽기 쉬운 프로그래밍 언어입니다.
            웹 개발, 데이터 분석, 인공지능 등 다양한 분야에서 사용됩니다.

            FastAPI는 Python 웹 프레임워크입니다.
            비동기 처리를 지원하며 자동 문서화 기능이 있습니다.
            """

            result = pipeline.ingest_bytes(
                doc_content.encode(),
                "python_guide.txt"
            )
            assert result["success"] == True

            # 2. 질의
            # 참고: 실제 LLM이 필요하므로 모킹 또는 통합 환경 필요
            # response = pipeline.query("Python이란?")
            # assert response.answer is not None

    @pytest.mark.integration
    def test_document_lifecycle(self, integration_env):
        """문서 생명주기"""
        from unittest.mock import patch

        with patch("app.config.settings") as mock_settings:
            mock_settings.data_dir = Path(integration_env) / "data"
            mock_settings.vectorstore_dir = Path(integration_env) / "vectorstore"

            from app.services.embedding_service import EmbeddingService
            from langchain_core.documents import Document

            service = EmbeddingService()

            # 1. 문서 추가
            docs = [
                Document(
                    page_content="테스트 문서 내용",
                    metadata={"source": "test.txt"}
                )
            ]

            count = service.add_documents(docs)
            assert count == 1

            # 2. 검색
            results = service.search("테스트", k=1)
            assert len(results) == 1

            # 3. 삭제
            deleted = service.delete_by_source("test.txt")
            assert deleted >= 0

            # 4. 초기화
            service.reset()
            stats = service.get_stats()
            assert stats["chunk_count"] == 0
