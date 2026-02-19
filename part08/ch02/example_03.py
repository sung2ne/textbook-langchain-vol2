# app/api/routes/system.py
from fastapi import APIRouter, Depends
from app.models.schemas import HealthResponse, StatsResponse
from app.services.rag_service import RAGService
from app.services.document_service import DocumentService
from app.api.dependencies import get_rag_service, get_document_service


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(
    rag_service: RAGService = Depends(get_rag_service)
):
    """헬스 체크"""
    return HealthResponse(
        status="healthy",
        vectorstore_ready=rag_service.is_ready(),
        document_count=rag_service.document_count()
    )


@router.get("/stats", response_model=StatsResponse)
async def get_stats(
    rag_service: RAGService = Depends(get_rag_service),
    document_service: DocumentService = Depends(get_document_service)
):
    """시스템 통계"""
    return StatsResponse(
        document_count=document_service.document_count(),
        chunk_count=rag_service.chunk_count(),
        vectorstore_size_mb=rag_service.vectorstore_size_mb()
    )


@router.post("/reset")
async def reset_system(
    rag_service: RAGService = Depends(get_rag_service),
    document_service: DocumentService = Depends(get_document_service)
):
    """시스템 초기화

    모든 문서와 벡터 저장소를 삭제합니다.
    """
    rag_service.reset()
    document_service.reset()

    return {"status": "reset", "message": "시스템이 초기화되었습니다."}
