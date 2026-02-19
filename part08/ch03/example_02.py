# app/services/chunking_service.py
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.config import settings


class ChunkingService:
    """문서 청킹 서비스"""

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def split_text(self, text: str, metadata: dict = None) -> List[Document]:
        """텍스트 분할"""
        chunks = self.splitter.split_text(text)

        documents = []
        for i, chunk in enumerate(chunks):
            doc_metadata = metadata.copy() if metadata else {}
            doc_metadata["chunk_index"] = i
            doc_metadata["chunk_total"] = len(chunks)

            documents.append(Document(
                page_content=chunk,
                metadata=doc_metadata
            ))

        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """문서 리스트 분할"""
        return self.splitter.split_documents(documents)


class SmartChunker:
    """스마트 청킹 (문서 타입별)"""

    def __init__(self):
        self.default_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )

        # 코드용 스플리터
        self.code_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\nclass ", "\ndef ", "\n\n", "\n"]
        )

        # 마크다운용 스플리터
        self.markdown_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n## ", "\n### ", "\n\n", "\n"]
        )

    def chunk(self, text: str, doc_type: str,
             metadata: dict = None) -> List[Document]:
        """문서 타입별 청킹"""
        # 스플리터 선택
        if doc_type in ["py", "python", "js", "java"]:
            splitter = self.code_splitter
        elif doc_type in ["md", "markdown"]:
            splitter = self.markdown_splitter
        else:
            splitter = self.default_splitter

        chunks = splitter.split_text(text)

        documents = []
        for i, chunk in enumerate(chunks):
            doc_metadata = metadata.copy() if metadata else {}
            doc_metadata.update({
                "chunk_index": i,
                "doc_type": doc_type
            })

            documents.append(Document(
                page_content=chunk,
                metadata=doc_metadata
            ))

        return documents
