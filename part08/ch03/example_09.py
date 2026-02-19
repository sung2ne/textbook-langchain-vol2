# app/api/routes/query.py (업데이트)
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.api.dependencies import get_pipeline
from app.services.pipeline_service import RAGPipeline
from app.models.schemas import QueryRequest, QueryResponse
import json

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    pipeline: RAGPipeline = Depends(get_pipeline)
):
    """질의응답"""
    return pipeline.query(request.question, request.k)


@router.get("/stream")
async def stream_query(
    question: str,
    k: int = 5,
    pipeline: RAGPipeline = Depends(get_pipeline)
):
    """스트리밍 질의"""
    async def generate():
        for chunk in pipeline.stream_query(question, k):
            yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
