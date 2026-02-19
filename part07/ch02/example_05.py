from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json


app = FastAPI()


async def stream_answer(question: str):
    """답변 스트리밍"""
    # 검색
    results = rag_service.search(question, k=5)

    if not results:
        yield f"data: {json.dumps({'type': 'error', 'content': '문서 없음'})}\n\n"
        return

    contexts = [r["content"] for r in results]
    context_text = "\n\n".join(contexts)

    prompt = f"""컨텍스트:
{context_text}

질문: {question}

답변:"""

    # 스트리밍 응답
    yield f"data: {json.dumps({'type': 'sources', 'content': results})}\n\n"

    # LLM 스트리밍 (Ollama 사용)
    from langchain_ollama import OllamaLLM

    llm = OllamaLLM(model="llama4")

    for chunk in llm.stream(prompt):
        yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"

    yield f"data: {json.dumps({'type': 'done'})}\n\n"


@app.get("/stream")
async def stream_query(question: str):
    """스트리밍 질의응답"""
    return StreamingResponse(
        stream_answer(question),
        media_type="text/event-stream"
    )
