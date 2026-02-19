from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


app = FastAPI()


# 커스텀 예외
class RAGException(Exception):
    def __init__(self, message: str, code: str = "RAG_ERROR"):
        self.message = message
        self.code = code


class DocumentNotFoundError(RAGException):
    def __init__(self, message: str = "문서를 찾을 수 없습니다"):
        super().__init__(message, "DOCUMENT_NOT_FOUND")


class VectorStoreError(RAGException):
    def __init__(self, message: str = "벡터 스토어 오류"):
        super().__init__(message, "VECTORSTORE_ERROR")


# 예외 핸들러
@app.exception_handler(RAGException)
async def rag_exception_handler(request: Request, exc: RAGException):
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.code,
            "message": exc.message
        }
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "details": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_ERROR",
            "message": "서버 내부 오류가 발생했습니다"
        }
    )


# 사용 예시
@app.post("/query")
async def query(request: QueryRequest):
    if rag_service.vectorstore is None:
        raise VectorStoreError("벡터 스토어가 초기화되지 않았습니다")

    return rag_service.query(request.question, request.k)
