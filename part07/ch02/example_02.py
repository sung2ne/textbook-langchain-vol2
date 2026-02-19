from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.documents import Document
from typing import List, Dict, Optional
import time


class RAGService:
    """RAG 서비스"""

    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.llm = OllamaLLM(model="llama4")
        self.vectorstore: Optional[Chroma] = None
        self.documents: List[Document] = []

    def add_documents(self, documents: List[Document]):
        """문서 추가"""
        self.documents.extend(documents)

        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                documents,
                self.embeddings
            )
        else:
            self.vectorstore.add_documents(documents)

    def search(self, query: str, k: int = 5) -> List[Dict]:
        """검색"""
        if self.vectorstore is None:
            return []

        results = self.vectorstore.similarity_search_with_score(query, k=k)

        return [
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "score": float(1 - score)
            }
            for doc, score in results
        ]

    def generate(self, query: str, contexts: List[str]) -> str:
        """답변 생성"""
        context_text = "\n\n".join(contexts)

        prompt = f"""다음 컨텍스트를 바탕으로 질문에 답하세요.

컨텍스트:
{context_text}

질문: {query}

답변:"""

        return self.llm.invoke(prompt)

    def query(self, question: str, k: int = 5) -> Dict:
        """질의응답"""
        start = time.time()

        # 검색
        results = self.search(question, k)

        if not results:
            return {
                "answer": "관련 문서를 찾을 수 없습니다.",
                "sources": [],
                "latency_ms": (time.time() - start) * 1000
            }

        # 컨텍스트 추출
        contexts = [r["content"] for r in results]

        # 답변 생성
        answer = self.generate(question, contexts)

        return {
            "answer": answer,
            "sources": results,
            "latency_ms": (time.time() - start) * 1000
        }

    def get_stats(self) -> Dict:
        """통계"""
        return {
            "document_count": len(self.documents),
            "vectorstore_ready": self.vectorstore is not None
        }


# 서비스 인스턴스 (싱글톤)
rag_service = RAGService()
