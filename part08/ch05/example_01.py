# tests/conftest.py
import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    """임시 디렉토리"""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.fixture
def sample_text():
    """샘플 텍스트"""
    return """
    LangChain은 대규모 언어 모델(LLM)을 활용한 애플리케이션 개발을 위한
    프레임워크입니다. 체인, 에이전트, 메모리 등 다양한 기능을 제공합니다.

    RAG(Retrieval-Augmented Generation)는 검색과 생성을 결합한 기술로,
    외부 지식을 활용하여 더 정확한 답변을 생성합니다.
    """


@pytest.fixture
def sample_documents(sample_text):
    """샘플 문서"""
    from langchain_core.documents import Document

    return [
        Document(
            page_content=sample_text,
            metadata={"source": "test.txt", "page": 1}
        )
    ]


@pytest.fixture
def mock_settings(temp_dir):
    """모의 설정"""
    from app.config import Settings

    return Settings(
        data_dir=Path(temp_dir) / "data",
        vectorstore_dir=Path(temp_dir) / "vectorstore",
        uploads_dir=Path(temp_dir) / "uploads"
    )
