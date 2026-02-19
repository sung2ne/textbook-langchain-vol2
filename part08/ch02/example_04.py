# app/services/document_service.py
from typing import List, Optional, Dict
from datetime import datetime
import tempfile
import os
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LCDocument

from app.config import Settings
from app.models.document import Document
from app.models.schemas import DocumentInfo, DocumentUploadResponse


class DocumentService:
    """문서 서비스"""

    def __init__(self, settings: Settings, rag_service):
        self.settings = settings
        self.rag_service = rag_service
        self.documents: Dict[str, Document] = {}

        # 텍스트 분할기
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )

    async def process_upload(self, filename: str, content: bytes) -> DocumentUploadResponse:
        """파일 업로드 처리"""
        # 임시 파일 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # 파일 로드
            documents = self._load_file(tmp_path, filename)

            if not documents:
                raise ValueError("문서를 읽을 수 없습니다.")

            # 청킹
            chunks = self.splitter.split_documents(documents)

            # 문서 ID 생성
            doc_id = Document.create_id(filename)

            # 메타데이터 추가
            for i, chunk in enumerate(chunks):
                chunk.metadata["document_id"] = doc_id
                chunk.metadata["filename"] = filename
                chunk.metadata["chunk_index"] = i

            # 벡터 스토어에 추가
            self.rag_service.add_documents(chunks)

            # 문서 정보 저장
            doc = Document(
                id=doc_id,
                filename=filename,
                content="",  # 원본 저장하지 않음
                chunks=len(chunks),
                size_bytes=len(content)
            )
            self.documents[doc_id] = doc

            return DocumentUploadResponse(
                id=doc_id,
                filename=filename,
                chunks=len(chunks),
                status="success"
            )

        finally:
            os.unlink(tmp_path)

    def _load_file(self, file_path: str, filename: str) -> List[LCDocument]:
        """파일 로드"""
        ext = Path(filename).suffix.lower()

        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext in [".txt", ".md"]:
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"지원하지 않는 파일 형식: {ext}")

        return loader.load()

    def list_documents(self) -> List[DocumentInfo]:
        """문서 목록"""
        return [
            DocumentInfo(
                id=doc.id,
                filename=doc.filename,
                chunks=doc.chunks,
                uploaded_at=doc.uploaded_at,
                size_bytes=doc.size_bytes
            )
            for doc in self.documents.values()
        ]

    def get_document(self, document_id: str) -> Optional[Document]:
        """문서 조회"""
        return self.documents.get(document_id)

    def delete_document(self, document_id: str) -> bool:
        """문서 삭제"""
        if document_id not in self.documents:
            return False

        # 벡터 스토어에서 삭제
        self.rag_service.delete_by_document_id(document_id)

        # 문서 정보 삭제
        del self.documents[document_id]

        return True

    def document_count(self) -> int:
        """문서 수"""
        return len(self.documents)

    def reset(self):
        """초기화"""
        self.documents.clear()
