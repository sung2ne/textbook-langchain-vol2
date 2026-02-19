# app/models/document.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict
import hashlib


@dataclass
class Document:
    """문서 클래스"""
    id: str
    filename: str
    content: str
    chunks: int
    size_bytes: int
    uploaded_at: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)

    @classmethod
    def create_id(cls, filename: str) -> str:
        """문서 ID 생성"""
        timestamp = datetime.now().isoformat()
        hash_input = f"{filename}_{timestamp}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]


@dataclass
class Chunk:
    """청크 클래스"""
    id: str
    document_id: str
    content: str
    index: int
    metadata: Dict = field(default_factory=dict)

    @classmethod
    def create_id(cls, document_id: str, index: int) -> str:
        """청크 ID 생성"""
        return f"{document_id}_{index:04d}"
