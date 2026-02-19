# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import documents, query, system


def create_app() -> FastAPI:
    """애플리케이션 생성"""
    app = FastAPI(
        title=settings.app_name,
        description="기술 문서 Q&A 시스템 API",
        version="1.0.0"
    )

    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록
    app.include_router(documents.router, prefix="/api/documents", tags=["문서"])
    app.include_router(query.router, prefix="/api", tags=["질의"])
    app.include_router(system.router, prefix="/api", tags=["시스템"])

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
