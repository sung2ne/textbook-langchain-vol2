from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from typing import List
import tempfile
import os


app = FastAPI(title="RAG API")


# 요청/응답 모델
class QueryRequest(BaseModel):
    question: str
    k: int = 5


class DocumentInfo(BaseModel):
    filename: str
    chunks: int
    status: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    latency_ms: float


class StatsResponse(BaseModel):
    document_count: int
    vectorstore_ready: bool


# 질의응답
@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """질문에 대한 답변 생성"""
    try:
        result = rag_service.query(request.question, request.k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 문서 업로드
@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """문서 업로드"""
    # 지원 형식 확인
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. PDF 또는 TXT만 지원합니다."
        )

    # 임시 파일 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # 파일 처리
        from langchain_community.document_loaders import PyPDFLoader, TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        if file.filename.endswith(".pdf"):
            loader = PyPDFLoader(tmp_path)
        else:
            loader = TextLoader(tmp_path, encoding="utf-8")

        documents = loader.load()

        # 분할
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)

        # 소스 메타데이터 추가
        for chunk in chunks:
            chunk.metadata["source"] = file.filename

        # 벡터 스토어에 추가
        rag_service.add_documents(chunks)

        return {
            "filename": file.filename,
            "chunks": len(chunks),
            "status": "success"
        }

    finally:
        os.unlink(tmp_path)


# 문서 목록
@app.get("/documents")
async def list_documents():
    """업로드된 문서 목록"""
    sources = set()
    for doc in rag_service.documents:
        sources.add(doc.metadata.get("source", "unknown"))

    return {
        "documents": list(sources),
        "total_chunks": len(rag_service.documents)
    }


# 통계
@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """시스템 통계"""
    return rag_service.get_stats()


# 검색만
@app.post("/search")
async def search(request: QueryRequest):
    """검색만 수행 (답변 생성 없이)"""
    results = rag_service.search(request.question, request.k)
    return {"results": results}


# 헬스 체크
@app.get("/health")
async def health():
    """헬스 체크"""
    return {
        "status": "healthy",
        "vectorstore": rag_service.vectorstore is not None
    }
