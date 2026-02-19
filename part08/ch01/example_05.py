# app/api/dependencies.py
from functools import lru_cache
from app.config import Settings, settings
from app.services.rag_service import RAGService
from app.services.document_service import DocumentService


@lru_cache
def get_settings() -> Settings:
    """설정 가져오기"""
    return settings


# 서비스 인스턴스 (싱글톤)
_rag_service: RAGService = None
_document_service: DocumentService = None


def get_rag_service() -> RAGService:
    """RAG 서비스 가져오기"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService(settings)
    return _rag_service


def get_document_service() -> DocumentService:
    """문서 서비스 가져오기"""
    global _document_service
    if _document_service is None:
        _document_service = DocumentService(settings, get_rag_service())
    return _document_service
