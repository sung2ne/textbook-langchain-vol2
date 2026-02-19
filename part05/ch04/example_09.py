from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.documents import Document
from typing import List, Dict
import re


class TechDocMultimodalRAG:
    """기술 문서 멀티모달 RAG"""

    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.llm = OllamaLLM(model="llama4")
        self.vectorstore = None
        self.code_blocks: List[Dict] = []
        self.diagrams: List[Dict] = []

    def add_markdown(self, content: str, source: str):
        """마크다운 문서 추가"""
        documents = []

        # 코드 블록 추출
        code_pattern = r'
