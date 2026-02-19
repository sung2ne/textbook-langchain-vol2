from pathlib import Path
from langchain_core.documents import Document


class MultiFormatLoader:
    """다중 형식 문서 로더"""

    def __init__(self, directory: str):
        self.directory = Path(directory)

    def load(self) -> List[Document]:
        """모든 지원 형식 로드"""
        documents = []

        # 텍스트 파일
        documents.extend(self._load_text())

        # PDF 파일
        documents.extend(self._load_pdf())

        # Markdown 파일
        documents.extend(self._load_markdown())

        return documents

    def _load_text(self) -> List[Document]:
        docs = []
        for file_path in self.directory.glob("**/*.txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            docs.append(Document(
                page_content=content,
                metadata={"source": str(file_path), "type": "text"}
            ))
        return docs

    def _load_pdf(self) -> List[Document]:
        docs = []
        try:
            from langchain_community.document_loaders import PyPDFLoader
            for file_path in self.directory.glob("**/*.pdf"):
                loader = PyPDFLoader(str(file_path))
                pages = loader.load()
                for page in pages:
                    page.metadata["type"] = "pdf"
                docs.extend(pages)
        except ImportError:
            print("PDF 로딩을 위해 pypdf를 설치하세요")
        return docs

    def _load_markdown(self) -> List[Document]:
        docs = []
        for file_path in self.directory.glob("**/*.md"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            docs.append(Document(
                page_content=content,
                metadata={"source": str(file_path), "type": "markdown"}
            ))
        return docs


# 사용
loader = MultiFormatLoader("./documents")
documents = loader.load()

# 형식별 통계
by_type = {}
for doc in documents:
    doc_type = doc.metadata.get("type", "unknown")
    by_type[doc_type] = by_type.get(doc_type, 0) + 1

print("형식별 문서 수:")
for doc_type, count in by_type.items():
    print(f"  {doc_type}: {count}개")
