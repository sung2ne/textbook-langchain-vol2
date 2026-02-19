# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_check():
    """헬스 체크 테스트"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_upload_document():
    """문서 업로드 테스트"""
    content = b"This is a test document."
    files = {"file": ("test.txt", content, "text/plain")}

    response = client.post("/api/documents/upload", files=files)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert data["filename"] == "test.txt"


def test_query_without_documents():
    """문서 없이 질의 테스트"""
    # 먼저 시스템 초기화
    client.post("/api/reset")

    response = client.post(
        "/api/query",
        json={"question": "테스트 질문", "k": 5}
    )
    assert response.status_code == 200

    data = response.json()
    assert "문서를 찾을 수 없습니다" in data["answer"]


def test_search():
    """검색 테스트"""
    response = client.post(
        "/api/search",
        json={"query": "test", "k": 5}
    )
    assert response.status_code == 200


def test_document_list():
    """문서 목록 테스트"""
    response = client.get("/api/documents")
    assert response.status_code == 200

    data = response.json()
    assert "documents" in data
    assert "total" in data


# 실행: pytest tests/test_api.py -v
