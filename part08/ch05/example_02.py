# tests/test_services.py
import pytest
from app.services.chunking_service import ChunkingService, SmartChunker
from app.services.loader_service import LoaderService


class TestChunkingService:
    """청킹 서비스 테스트"""

    def test_split_text(self, sample_text):
        """텍스트 분할 테스트"""
        service = ChunkingService()
        chunks = service.split_text(sample_text, {"source": "test"})

        assert len(chunks) > 0
        assert all(doc.metadata.get("source") == "test" for doc in chunks)
        assert all("chunk_index" in doc.metadata for doc in chunks)

    def test_split_with_metadata(self):
        """메타데이터 포함 분할"""
        service = ChunkingService()
        text = "짧은 텍스트입니다."
        metadata = {"source": "test.txt", "page": 1}

        chunks = service.split_text(text, metadata)

        assert len(chunks) == 1
        assert chunks[0].metadata["source"] == "test.txt"
        assert chunks[0].metadata["page"] == 1


class TestSmartChunker:
    """스마트 청커 테스트"""

    def test_code_chunking(self):
        """코드 청킹"""
        chunker = SmartChunker()
        code = """
def hello():
    print("Hello")

def world():
    print("World")
"""
        chunks = chunker.chunk(code, "py", {"source": "code.py"})

        assert len(chunks) > 0
        assert chunks[0].metadata["doc_type"] == "py"

    def test_markdown_chunking(self):
        """마크다운 청킹"""
        chunker = SmartChunker()
        md = """
## 제목 1
내용 1

## 제목 2
내용 2
"""
        chunks = chunker.chunk(md, "md", {"source": "doc.md"})

        assert len(chunks) > 0
        assert chunks[0].metadata["doc_type"] == "md"


class TestLoaderService:
    """로더 서비스 테스트"""

    def test_load_text(self, temp_dir):
        """텍스트 파일 로드"""
        from pathlib import Path

        # 파일 생성
        file_path = Path(temp_dir) / "test.txt"
        file_path.write_text("테스트 내용입니다.", encoding="utf-8")

        loader = LoaderService()
        content, doc_type = loader.load(str(file_path))

        assert content == "테스트 내용입니다."
        assert doc_type == "txt"

    def test_load_bytes(self):
        """바이트에서 로드"""
        loader = LoaderService()
        content = "바이트 내용".encode("utf-8")

        text, doc_type = loader.load_bytes(content, "test.txt")

        assert text == "바이트 내용"
        assert doc_type == "txt"

    def test_unsupported_format(self, temp_dir):
        """지원하지 않는 형식"""
        from pathlib import Path

        file_path = Path(temp_dir) / "test.xyz"
        file_path.touch()

        loader = LoaderService()

        with pytest.raises(ValueError):
            loader.load(str(file_path))
