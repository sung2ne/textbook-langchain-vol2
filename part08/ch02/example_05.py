# app/services/rag_service.py
from typing import List, Dict, Optional, Generator
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.documents import Document
from app.config import Settings
from app.models.schemas import QueryResponse, Source, SearchResult
import time
import json
import os


class RAGService:
    """RAG 서비스"""

    def __init__(self, settings: Settings):
        self.settings = settings

        # 임베딩 모델
        self.embeddings = OllamaEmbeddings(
            model=settings.embedding_model
        )

        # LLM
        self.llm = OllamaLLM(
            model=settings.llm_model,
            temperature=0.7
        )

        # 벡터 스토어
        self.vectorstore: Optional[Chroma] = None
        self._init_vectorstore()

    def _init_vectorstore(self):
        """벡터 스토어 초기화"""
        persist_dir = str(self.settings.vectorstore_dir)

        # 기존 저장소 로드 또는 새로 생성
        if os.path.exists(persist_dir) and os.listdir(persist_dir):
            self.vectorstore = Chroma(
                persist_directory=persist_dir,
                embedding_function=self.embeddings
            )
        else:
            self.vectorstore = None

    def add_documents(self, documents: List[Document]):
        """문서 추가"""
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                documents,
                self.embeddings,
                persist_directory=str(self.settings.vectorstore_dir)
            )
        else:
            self.vectorstore.add_documents(documents)

    def search(self, query: str, k: int = 5) -> List[SearchResult]:
        """검색"""
        if self.vectorstore is None:
            return []

        results = self.vectorstore.similarity_search_with_score(query, k=k)

        return [
            SearchResult(
                content=doc.page_content,
                source=doc.metadata.get("filename", "unknown"),
                score=float(1 - score),  # 거리를 유사도로 변환
                metadata=doc.metadata
            )
            for doc, score in results
        ]

    def query(self, question: str, k: int = 5) -> QueryResponse:
        """질의응답"""
        start_time = time.time()

        # 검색
        results = self.search(question, k)

        if not results:
            return QueryResponse(
                answer="관련 문서를 찾을 수 없습니다. 먼저 문서를 업로드해주세요.",
                sources=[],
                latency_ms=(time.time() - start_time) * 1000
            )

        # 컨텍스트 구성
        contexts = [r.content for r in results]
        context_text = "\n\n".join(contexts)

        # 프롬프트
        prompt = f"""다음 컨텍스트를 바탕으로 질문에 답하세요.
컨텍스트에 없는 정보는 "알 수 없습니다"라고 답하세요.

컨텍스트:
{context_text}

질문: {question}

답변:"""

        # 답변 생성
        answer = self.llm.invoke(prompt)

        # 출처 구성
        sources = [
            Source(
                content=r.content[:200],
                source=r.source,
                page=r.metadata.get("page"),
                score=r.score
            )
            for r in results
        ]

        return QueryResponse(
            answer=answer,
            sources=sources,
            latency_ms=(time.time() - start_time) * 1000
        )

    def stream_query(self, question: str, k: int = 5) -> Generator[str, None, None]:
        """스트리밍 질의응답"""
        # 검색
        results = self.search(question, k)

        # 출처 전송
        sources = [
            {
                "content": r.content[:200],
                "source": r.source,
                "score": r.score
            }
            for r in results
        ]
        yield f"data: {json.dumps({'type': 'sources', 'data': sources})}\n\n"

        if not results:
            yield f"data: {json.dumps({'type': 'error', 'data': '문서 없음'})}\n\n"
            return

        # 프롬프트 구성
        context_text = "\n\n".join(r.content for r in results)
        prompt = f"""컨텍스트:
{context_text}

질문: {question}

답변:"""

        # 스트리밍 생성
        for chunk in self.llm.stream(prompt):
            yield f"data: {json.dumps({'type': 'token', 'data': chunk})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    def delete_by_document_id(self, document_id: str):
        """문서 ID로 삭제"""
        if self.vectorstore is None:
            return

        # ChromaDB에서 문서 삭제
        self.vectorstore._collection.delete(
            where={"document_id": document_id}
        )

    def is_ready(self) -> bool:
        """준비 상태"""
        return self.vectorstore is not None

    def document_count(self) -> int:
        """문서 수 (고유 문서 ID 기준)"""
        if self.vectorstore is None:
            return 0

        # 메타데이터에서 고유 document_id 추출
        collection = self.vectorstore._collection
        if collection.count() == 0:
            return 0

        results = collection.get(include=["metadatas"])
        doc_ids = set()
        for metadata in results.get("metadatas", []):
            if metadata and "document_id" in metadata:
                doc_ids.add(metadata["document_id"])

        return len(doc_ids)

    def chunk_count(self) -> int:
        """청크 수"""
        if self.vectorstore is None:
            return 0
        return self.vectorstore._collection.count()

    def vectorstore_size_mb(self) -> float:
        """벡터 스토어 크기 (MB)"""
        persist_dir = self.settings.vectorstore_dir
        if not persist_dir.exists():
            return 0.0

        total_size = sum(
            f.stat().st_size for f in persist_dir.rglob("*") if f.is_file()
        )
        return total_size / (1024 * 1024)

    def reset(self):
        """초기화"""
        if self.vectorstore is not None:
            # 모든 데이터 삭제
            self.vectorstore._collection.delete(where={})

        self.vectorstore = None
