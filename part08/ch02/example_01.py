# app/api/routes/documents.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from app.models.schemas import (
    DocumentUploadResponse,
    DocumentListResponse,
    DocumentInfo
)
from app.services.document_service import DocumentService
from app.api.dependencies import get_document_service


router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service)
):
    """문서 업로드

    PDF, TXT, MD 파일을 업로드합니다.
    """
    # 파일 형식 검증
    allowed_extensions = {".pdf", ".txt", ".md"}
    file_ext = "." + file.filename.split(".")[-1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 파일 형식입니다. 허용: {allowed_extensions}"
        )

    # 파일 크기 제한 (10MB)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="파일 크기가 10MB를 초과합니다."
        )

    try:
        result = await document_service.process_upload(file.filename, content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    document_service: DocumentService = Depends(get_document_service)
):
    """문서 목록 조회"""
    documents = document_service.list_documents()
    return DocumentListResponse(
        documents=documents,
        total=len(documents)
    )


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    document_service: DocumentService = Depends(get_document_service)
):
    """문서 상세 조회"""
    document = document_service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")

    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    document_service: DocumentService = Depends(get_document_service)
):
    """문서 삭제"""
    success = document_service.delete_document(document_id)

    if not success:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다.")

    return {"status": "deleted", "document_id": document_id}
