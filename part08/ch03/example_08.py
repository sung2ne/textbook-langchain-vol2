# app/api/dependencies.py
from functools import lru_cache
from app.config import Settings, settings
from app.services.pipeline_service import RAGPipeline, PipelineConfig


@lru_cache
def get_settings() -> Settings:
    """설정"""
    return settings


# 파이프라인 인스턴스
_pipeline: RAGPipeline = None


def get_pipeline() -> RAGPipeline:
    """파이프라인"""
    global _pipeline
    if _pipeline is None:
        config = PipelineConfig(
            use_cache=True,
            min_score=0.0,
            max_sources=settings.top_k
        )
        _pipeline = RAGPipeline(config)
    return _pipeline
