# app/config.py
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # 앱 설정
    app_name: str = "Tech Docs Q&A"
    debug: bool = False

    # 모델 설정
    llm_model: str = "llama4"
    embedding_model: str = "nomic-embed-text"

    # RAG 설정
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 5

    # 경로 설정
    data_dir: Path = Path("./data")
    vectorstore_dir: Path = Path("./data/vectorstore")
    uploads_dir: Path = Path("./data/uploads")

    # API 설정
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    class Config:
        env_file = ".env"


# 설정 인스턴스
settings = Settings()

# 디렉토리 생성
settings.data_dir.mkdir(exist_ok=True)
settings.vectorstore_dir.mkdir(exist_ok=True)
settings.uploads_dir.mkdir(exist_ok=True)
