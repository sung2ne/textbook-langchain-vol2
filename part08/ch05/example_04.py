# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock


@pytest.fixture
def client():
    """테스트 클라이언트"""
    from app.main import app
    return TestClient(app)


class TestSystemAPI:
    """시스템 API 테스트"""

    def test_health(self, client):
        """헬스 체크"""
        response = client.get("/api/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "vectorstore_ready" in data

    def test_stats(self, client):
        """통계"""
        response = client.get("/api/stats")

        assert response.status_code == 200
        data = response.json()
        assert "document_count" in data
        assert "chunk_count" in data


class TestDocumentAPI:
    """문서 API 테스트"""

    def test_list_documents(self, client):
        """문서 목록"""
        response = client.get("/api/documents")

        assert response.status_code == 200
        data = response.json()
        assert "documents" in data
        assert "total" in data

    @patch("app.api.dependencies.get_pipeline")
    def test_upload_document(self, mock_pipeline, client):
        """문서 업로드"""
        mock_pipeline.return_value.ingest_bytes.return_value = {
            "success": True,
            "source": "test.txt",
            "chunks": 5
        }

        files = {"file": ("test.txt", b"test content", "text/plain")}
        response = client.post("/api/documents/upload", files=files)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"


class TestQueryAPI:
    """질의 API 테스트"""

    @patch("app.api.dependencies.get_pipeline")
    def test_query(self, mock_pipeline, client):
        """질의"""
        from app.models.schemas import QueryResponse

        mock_pipeline.return_value.query.return_value = QueryResponse(
            answer="테스트 답변",
            sources=[],
            latency_ms=100.0
        )

        response = client.post(
            "/api/query",
            json={"question": "테스트 질문", "k": 5}
        )

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert data["answer"] == "테스트 답변"

    def test_query_validation(self, client):
        """질의 유효성 검사"""
        # 빈 질문
        response = client.post(
            "/api/query",
            json={"question": "", "k": 5}
        )

        assert response.status_code == 422  # Validation Error

    def test_stream_query(self, client):
        """스트리밍 질의"""
        response = client.get(
            "/api/stream",
            params={"question": "테스트", "k": 5}
        )

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/event-stream")
