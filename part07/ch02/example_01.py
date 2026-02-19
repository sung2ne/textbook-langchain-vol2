from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="RAG API",
    description="RAG 시스템 API",
    version="1.0.0"
)


# 요청/응답 모델
class QueryRequest(BaseModel):
    question: str
    k: int = 5


class Source(BaseModel):
    content: str
    source: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    latency_ms: float


# 엔드포인트
@app.get("/")
async def root():
    return {"message": "RAG API", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# 실행: uvicorn main:app --reload
