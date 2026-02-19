# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# 문서 관련
class DocumentUploadResponse(BaseModel):
    """문서 업로드 응답"""
    id: str
    filename: str
    chunks: int
    status: str


class DocumentInfo(BaseModel):
    """문서 정보"""
    id: str
    filename: str
    chunks: int
    uploaded_at: datetime
    size_bytes: int


class DocumentListResponse(BaseModel):
    """문서 목록 응답"""
    documents: List[DocumentInfo]
    total: int


# 질의 관련
class QueryRequest(BaseModel):
    """질의 요청"""
    question: str = Field(..., min_length=1, max_length=1000)
    k: int = Field(default=5, ge=1, le=20)


class Source(BaseModel):
    """출처 정보"""
    content: str
    source: str
    page: Optional[int] = None
    score: float


class QueryResponse(BaseModel):
    """질의 응답"""
    answer: str
    sources: List[Source]
    latency_ms: float


# 검색 관련
class SearchRequest(BaseModel):
    """검색 요청"""
    query: str = Field(..., min_length=1)
    k: int = Field(default=10, ge=1, le=50)


class SearchResult(BaseModel):
    """검색 결과"""
    content: str
    source: str
    score: float
    metadata: dict


class SearchResponse(BaseModel):
    """검색 응답"""
    results: List[SearchResult]
    total: int


# 시스템 관련
class HealthResponse(BaseModel):
    """헬스 체크 응답"""
    status: str
    vectorstore_ready: bool
    document_count: int


class StatsResponse(BaseModel):
    """통계 응답"""
    document_count: int
    chunk_count: int
    vectorstore_size_mb: float
