# app/api/routes/query.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.models.schemas import (
    QueryRequest,
    QueryResponse,
    SearchRequest,
    SearchResponse
)
from app.services.rag_service import RAGService
from app.api.dependencies import get_rag_service
import json


router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """질의응답

    질문에 대한 답변을 생성합니다.
    """
    try:
        result = rag_service.query(request.question, request.k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stream")
async def stream_query(
    question: str,
    k: int = 5,
    rag_service: RAGService = Depends(get_rag_service)
):
    """스트리밍 질의응답

    답변을 실시간으로 스트리밍합니다.
    """
    return StreamingResponse(
        rag_service.stream_query(question, k),
        media_type="text/event-stream"
    )


@router.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """검색

    관련 문서를 검색합니다 (답변 생성 없이).
    """
    results = rag_service.search(request.query, request.k)
    return SearchResponse(
        results=results,
        total=len(results)
    )
