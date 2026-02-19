from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
import json
import asyncio


app = FastAPI()


class StreamingRAG:
    """스트리밍 RAG"""

    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.llm = OllamaLLM(model="llama4")
        self.vectorstore = None

    def add_documents(self, documents):
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(documents, self.embeddings)
        else:
            self.vectorstore.add_documents(documents)

    async def stream_query(self, question: str, k: int = 5):
        """스트리밍 질의"""
        # 1. 검색 시작 신호
        yield self._format_sse({"type": "status", "data": "검색 중..."})

        # 2. 검색
        if self.vectorstore is None:
            yield self._format_sse({"type": "error", "data": "문서가 없습니다"})
            return

        results = self.vectorstore.similarity_search(question, k=k)

        # 3. 검색 결과 전송
        sources = [
            {
                "content": doc.page_content[:200],
                "source": doc.metadata.get("source", "unknown")
            }
            for doc in results
        ]
        yield self._format_sse({"type": "sources", "data": sources})

        # 4. 생성 시작
        yield self._format_sse({"type": "status", "data": "답변 생성 중..."})

        # 5. 프롬프트 구성
        context = "\n\n".join(doc.page_content for doc in results)
        prompt = f"""다음 컨텍스트를 바탕으로 질문에 답하세요.

컨텍스트:
{context}

질문: {question}

답변:"""

        # 6. LLM 스트리밍
        for chunk in self.llm.stream(prompt):
            yield self._format_sse({"type": "token", "data": chunk})
            await asyncio.sleep(0)

        # 7. 완료
        yield self._format_sse({"type": "done"})

    def _format_sse(self, data: dict) -> str:
        """SSE 포맷"""
        return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


# 인스턴스
streaming_rag = StreamingRAG()


@app.get("/stream/query")
async def stream_query(question: str, k: int = 5):
    """스트리밍 질의 엔드포인트"""
    return StreamingResponse(
        streaming_rag.stream_query(question, k),
        media_type="text/event-stream"
    )
