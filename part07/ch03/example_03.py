# rag_client/__init__.py
from .client import RAGClient

__all__ = ["RAGClient"]


# rag_client/client.py
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class QueryResult:
    """질의 결과"""
    answer: str
    sources: List[Dict]
    latency_ms: float


@dataclass
class SearchResult:
    """검색 결과"""
    content: str
    source: str
    score: float


class RAGClient:
    """RAG API 클라이언트"""

    def __init__(self, base_url: str = "http://localhost:8000",
                 timeout: int = 30, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.api_key = api_key
        self._session = requests.Session()

        if api_key:
            self._session.headers["X-API-Key"] = api_key

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """HTTP 요청"""
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)

        response = self._session.request(method, url, **kwargs)
        response.raise_for_status()

        return response

    def health(self) -> bool:
        """헬스 체크"""
        try:
            response = self._request("GET", "/health")
            return response.json().get("status") == "healthy"
        except:
            return False

    def query(self, question: str, k: int = 5) -> QueryResult:
        """질의응답"""
        response = self._request(
            "POST",
            "/query",
            json={"question": question, "k": k}
        )
        data = response.json()

        return QueryResult(
            answer=data["answer"],
            sources=data.get("sources", []),
            latency_ms=data.get("latency_ms", 0)
        )

    def search(self, query: str, k: int = 5) -> List[SearchResult]:
        """검색"""
        response = self._request(
            "POST",
            "/search",
            json={"question": query, "k": k}
        )

        results = response.json().get("results", [])

        return [
            SearchResult(
                content=r["content"],
                source=r.get("source", "unknown"),
                score=r.get("score", 0)
            )
            for r in results
        ]

    def upload(self, file_path: str) -> Dict:
        """파일 업로드"""
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = self._request("POST", "/documents/upload", files=files)

        return response.json()

    def documents(self) -> List[str]:
        """문서 목록"""
        response = self._request("GET", "/documents")
        return response.json().get("documents", [])

    def stats(self) -> Dict:
        """통계"""
        response = self._request("GET", "/stats")
        return response.json()


# 사용
if __name__ == "__main__":
    client = RAGClient("http://localhost:8000")

    # 헬스 체크
    if client.health():
        print("API 연결됨")

        # 질의
        result = client.query("LangChain이란?")
        print(f"답변: {result.answer}")
        print(f"출처: {len(result.sources)}개")
        print(f"응답 시간: {result.latency_ms:.0f}ms")
