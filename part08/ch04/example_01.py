# frontend/api_client.py
import requests
from typing import List, Optional, Generator
import json


class APIClient:
    """백엔드 API 클라이언트"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"

    def health_check(self) -> dict:
        """헬스 체크"""
        response = requests.get(f"{self.api_url}/health")
        return response.json()

    def get_stats(self) -> dict:
        """통계"""
        response = requests.get(f"{self.api_url}/stats")
        return response.json()

    # 문서 관련
    def upload_document(self, file) -> dict:
        """문서 업로드"""
        files = {"file": (file.name, file, file.type)}
        response = requests.post(
            f"{self.api_url}/documents/upload",
            files=files
        )
        return response.json()

    def list_documents(self) -> dict:
        """문서 목록"""
        response = requests.get(f"{self.api_url}/documents")
        return response.json()

    def delete_document(self, doc_id: str) -> dict:
        """문서 삭제"""
        response = requests.delete(f"{self.api_url}/documents/{doc_id}")
        return response.json()

    # 질의 관련
    def query(self, question: str, k: int = 5) -> dict:
        """질의응답"""
        response = requests.post(
            f"{self.api_url}/query",
            json={"question": question, "k": k}
        )
        return response.json()

    def stream_query(self, question: str,
                    k: int = 5) -> Generator[dict, None, None]:
        """스트리밍 질의"""
        response = requests.get(
            f"{self.api_url}/stream",
            params={"question": question, "k": k},
            stream=True
        )

        for line in response.iter_lines():
            if line:
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    yield data

    def search(self, query: str, k: int = 10) -> dict:
        """검색"""
        response = requests.post(
            f"{self.api_url}/search",
            json={"query": query, "k": k}
        )
        return response.json()

    def reset(self) -> dict:
        """시스템 초기화"""
        response = requests.post(f"{self.api_url}/reset")
        return response.json()


# 싱글톤 인스턴스
api_client = APIClient()
