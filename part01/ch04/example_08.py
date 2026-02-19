import os
from enum import Enum


class EmbeddingProvider(Enum):
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"
    OPENAI = "openai"


class EmbeddingConfig:
    """임베딩 설정 관리"""

    # 기본 설정
    DEFAULTS = {
        EmbeddingProvider.OLLAMA: {
            "model": "nomic-embed-text",
            "base_url": "http://localhost:11434"
        },
        EmbeddingProvider.HUGGINGFACE: {
            "model_name": "sentence-transformers/all-MiniLM-L6-v2",
            "device": "cpu"
        },
        EmbeddingProvider.OPENAI: {
            "model": "text-embedding-3-small"
        }
    }

    @classmethod
    def create_embeddings(cls, provider: EmbeddingProvider, **kwargs):
        """설정에 따른 임베딩 생성"""
        config = {**cls.DEFAULTS[provider], **kwargs}

        if provider == EmbeddingProvider.OLLAMA:
            from langchain_ollama import OllamaEmbeddings
            return OllamaEmbeddings(
                model=config["model"],
                base_url=config.get("base_url")
            )

        elif provider == EmbeddingProvider.HUGGINGFACE:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(
                model_name=config["model_name"],
                model_kwargs={"device": config.get("device", "cpu")}
            )

        elif provider == EmbeddingProvider.OPENAI:
            from langchain_openai import OpenAIEmbeddings
            return OpenAIEmbeddings(model=config["model"])

    @classmethod
    def from_env(cls):
        """환경변수에서 설정 로드"""
        provider_name = os.getenv("EMBEDDING_PROVIDER", "ollama")
        provider = EmbeddingProvider(provider_name)

        return cls.create_embeddings(provider)


# 사용
embeddings = EmbeddingConfig.create_embeddings(
    EmbeddingProvider.OLLAMA,
    model="mxbai-embed-large"
)

# 또는 환경변수로
# EMBEDDING_PROVIDER=huggingface
embeddings = EmbeddingConfig.from_env()
