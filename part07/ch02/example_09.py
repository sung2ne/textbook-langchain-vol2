# test_api.py
import requests
import json


BASE_URL = "http://localhost:8000"


def test_health():
    """헬스 체크 테스트"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("✓ Health check passed")


def test_upload_document():
    """문서 업로드 테스트"""
    with open("test.txt", "w") as f:
        f.write("LangChain은 LLM 프레임워크입니다.")

    with open("test.txt", "rb") as f:
        response = requests.post(
            f"{BASE_URL}/documents/upload",
            files={"file": ("test.txt", f, "text/plain")}
        )

    assert response.status_code == 200
    print("✓ Document upload passed")


def test_query():
    """질의응답 테스트"""
    response = requests.post(
        f"{BASE_URL}/query",
        json={"question": "LangChain이란?", "k": 3}
    )

    assert response.status_code == 200
    data = response.json()
    print(f"✓ Query passed: {data['answer'][:50]}...")


if __name__ == "__main__":
    test_health()
    test_upload_document()
    test_query()
    print("\n모든 테스트 통과!")
