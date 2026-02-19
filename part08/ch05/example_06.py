# tests/test_performance.py
import pytest
import time
from unittest.mock import patch


class TestPerformance:
    """성능 테스트"""

    @pytest.fixture
    def large_document(self):
        """대용량 문서"""
        return "이것은 테스트 문장입니다. " * 1000  # ~20KB

    @pytest.mark.performance
    def test_chunking_speed(self, large_document):
        """청킹 속도"""
        from app.services.chunking_service import ChunkingService

        service = ChunkingService()

        start = time.time()
        chunks = service.split_text(large_document, {"source": "test"})
        elapsed = time.time() - start

        assert elapsed < 1.0  # 1초 이내
        assert len(chunks) > 0

    @pytest.mark.performance
    def test_search_speed(self):
        """검색 속도"""
        # 벡터 저장소가 준비된 상태에서 검색 속도 테스트
        # 실제 환경에서는 더 큰 데이터셋으로 테스트
        pass

    @pytest.mark.performance
    def test_concurrent_queries(self):
        """동시 질의"""
        import concurrent.futures
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)

        def make_request():
            return client.get("/api/health")

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            results = [f.result() for f in futures]

        success_count = sum(1 for r in results if r.status_code == 200)
        assert success_count == 50
