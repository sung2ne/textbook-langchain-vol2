# app/config.py (Docker 환경 지원)
from pydantic_settings import BaseSettings
from pathlib import Path
import os


class Settings(BaseSettings):
    """Docker 환경 지원 설정"""

    # 앱 설정
    app_name: str = "Tech Docs Q&A"
    debug: bool = False
    log_level: str = "INFO"

    # Ollama 설정 (Docker에서는 서비스 이름 사용)
    ollama_host: str = "http://localhost:11434"
    llm_model: str = "llama4"
    embedding_model: str = "nomic-embed-text"

    # 경로 설정
    data_dir: Path = Path("/app/data")
    vectorstore_dir: Path = Path("/app/data/vectorstore")
    uploads_dir: Path = Path("/app/data/uploads")

    # RAG 설정
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 5

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 디렉토리 생성
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.vectorstore_dir.mkdir(parents=True, exist_ok=True)
        self.uploads_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
