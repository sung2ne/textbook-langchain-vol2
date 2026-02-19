from pathlib import Path
from langchain_core.documents import Document


class DocumentLoaderUtils:
    """문서 로더 유틸리티"""

    @staticmethod
    def load_text_files(directory: str, pattern: str = "*.txt") -> List[Document]:
        """텍스트 파일 로드"""
        documents = []
        path = Path(directory)

        for file_path in path.glob(pattern):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            doc = Document(
                page_content=content,
                metadata={"source": str(file_path), "filename": file_path.name}
            )
            documents.append(doc)

        return documents

    @staticmethod
    def load_from_dict_list(data: List[dict], content_key: str = "content") -> List[Document]:
        """딕셔너리 리스트에서 문서 생성"""
        documents = []

        for item in data:
            content = item.pop(content_key, "")
            doc = Document(page_content=content, metadata=item)
            documents.append(doc)

        return documents

    @staticmethod
    def merge_documents(documents: List[Document], separator: str = "\n\n") -> Document:
        """여러 문서를 하나로 병합"""
        merged_content = separator.join(doc.page_content for doc in documents)
        merged_metadata = {
            "source": "merged",
            "document_count": len(documents)
        }
        return Document(page_content=merged_content, metadata=merged_metadata)


# 사용
docs = DocumentLoaderUtils.load_text_files("./documents")
print(f"로드된 문서: {len(docs)}개")
