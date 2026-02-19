# app/api/routes/health.py
from fastapi import APIRouter
from app.services.embedding_service import EmbeddingService
import psutil

router = APIRouter()


@router.get("/health")
async def health():
    """기본 헬스체크"""
    return {"status": "healthy"}


@router.get("/health/detailed")
async def detailed_health():
    """상세 헬스체크"""
    embedding_service = EmbeddingService()
    stats = embedding_service.get_stats()

    # 시스템 리소스
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "status": "healthy",
        "vectorstore": {
            "ready": embedding_service.vectorstore is not None,
            "chunk_count": stats.get("chunk_count", 0)
        },
        "system": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "disk_percent": disk.percent,
            "disk_free_gb": round(disk.free / (1024**3), 2)
        }
    }


@router.get("/ready")
async def readiness():
    """준비 상태 (K8s readiness probe)"""
    embedding_service = EmbeddingService()

    if embedding_service.vectorstore is None:
        return {"ready": False, "reason": "Vectorstore not initialized"}

    return {"ready": True}


@router.get("/live")
async def liveness():
    """생존 상태 (K8s liveness probe)"""
    return {"alive": True}
