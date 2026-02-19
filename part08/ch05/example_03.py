# tests/test_pipeline.py
import pytest
from unittest.mock import Mock, patch


class TestRAGPipeline:
    """RAG 파이프라인 테스트"""

    @pytest.fixture
    def pipeline(self, temp_dir):
        """파이프라인 인스턴스"""
        with patch("app.services.pipeline_service.settings") as mock_settings:
            mock_settings.vectorstore_dir = temp_dir
            mock_settings.chunk_size = 100
            mock_settings.chunk_overlap = 10
            mock_settings.top_k = 3
            mock_settings.embedding_model = "nomic-embed-text"
            mock_settings.llm_model = "llama4"

            from app.services.pipeline_service import RAGPipeline, PipelineConfig

            config = PipelineConfig(use_cache=False)
            return RAGPipeline(config)

    def test_ingest_text(self, pipeline, temp_dir):
        """텍스트 수집 테스트"""
        from pathlib import Path

        # 파일 생성
        file_path = Path(temp_dir) / "test.txt"
        file_path.write_text("테스트 문서 내용입니다.", encoding="utf-8")

        result = pipeline.ingest(str(file_path))

        assert result["success"] == True
        assert result["chunks"] > 0

    def test_ingest_bytes(self, pipeline):
        """바이트 수집 테스트"""
        content = "바이트로 전달된 내용".encode("utf-8")

        result = pipeline.ingest_bytes(content, "test.txt")

        assert result["success"] == True

    @patch("app.services.chain_service.OllamaLLM")
    @patch("app.services.embedding_service.OllamaEmbeddings")
    def test_query(self, mock_embeddings, mock_llm, pipeline, sample_text):
        """질의 테스트"""
        # 모의 설정
        mock_llm.return_value.invoke.return_value = "모의 답변입니다."

        # 문서 추가
        pipeline.ingest_bytes(sample_text.encode(), "test.txt")

        # 질의
        response = pipeline.query("LangChain이란?", k=3)

        assert response.answer is not None
        assert isinstance(response.latency_ms, float)


class TestBatchPipeline:
    """배치 파이프라인 테스트"""

    @pytest.fixture
    def batch_pipeline(self, temp_dir):
        """배치 파이프라인"""
        with patch("app.services.pipeline_service.settings"):
            from app.services.pipeline_service import BatchPipeline
            return BatchPipeline()

    def test_ingest_directory(self, batch_pipeline, temp_dir):
        """디렉토리 수집"""
        from pathlib import Path

        # 파일 생성
        (Path(temp_dir) / "doc1.txt").write_text("문서 1")
        (Path(temp_dir) / "doc2.txt").write_text("문서 2")
        (Path(temp_dir) / "image.jpg").touch()  # 지원 안 함

        results = batch_pipeline.ingest_directory(temp_dir)

        # txt 파일만 수집
        success_count = sum(1 for r in results if r["success"])
        assert success_count == 2
