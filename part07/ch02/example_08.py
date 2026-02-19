from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn


# 앱 생성
app = FastAPI(
    title="RAG API",
    description="LangChain 기반 RAG 시스템 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 모델 정의
class QueryRequest(BaseModel):
    question: str
    k: int = 5


class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    latency_ms: float


class DocumentUploadResponse(BaseModel):
    filename: str
    chunks: int
    status: str


class StatsResponse(BaseModel):
    document_count: int
    vectorstore_ready: bool


# 라우터
@app.get("/", tags=["기본"])
async def root():
    """API 정보"""
    return {
        "name": "RAG API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["기본"])
async def health():
    """헬스 체크"""
    return {
        "status": "healthy",
        "vectorstore": rag_service.vectorstore is not None
    }


@app.post("/query", response_model=QueryResponse, tags=["질의응답"])
async def query(request: QueryRequest):
    """질문에 대한 답변 생성

    Args:
        request: 질문과 검색 파라미터

    Returns:
        답변, 출처, 응답 시간
    """
    try:
        result = rag_service.query(request.question, request.k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", tags=["검색"])
async def search(request: QueryRequest):
    """검색만 수행

    답변 생성 없이 관련 문서만 검색합니다.
    """
    results = rag_service.search(request.question, request.k)
    return {"results": results, "count": len(results)}


@app.post("/documents/upload", response_model=DocumentUploadResponse, tags=["문서"])
async def upload_document(file: UploadFile = File(...)):
    """문서 업로드

    PDF 또는 TXT 파일을 업로드하여 RAG 시스템에 추가합니다.
    """
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="PDF 또는 TXT만 지원")

    # 처리 로직 (이전 코드 참조)
    return {
        "filename": file.filename,
        "chunks": 0,  # 실제 처리 결과
        "status": "success"
    }


@app.get("/documents", tags=["문서"])
async def list_documents():
    """문서 목록 조회"""
    sources = set()
    for doc in rag_service.documents:
        sources.add(doc.metadata.get("source", "unknown"))

    return {
        "documents": list(sources),
        "total_chunks": len(rag_service.documents)
    }


@app.delete("/documents/{filename}", tags=["문서"])
async def delete_document(filename: str):
    """문서 삭제 (미구현)"""
    raise HTTPException(status_code=501, detail="Not implemented")


@app.get("/stats", response_model=StatsResponse, tags=["시스템"])
async def get_stats():
    """시스템 통계"""
    return rag_service.get_stats()


# 실행
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
