# app/api/routes/metrics.py
from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

router = APIRouter()


@router.get("/metrics")
async def metrics():
    """Prometheus 메트릭"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
