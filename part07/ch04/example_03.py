from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_ollama import OllamaLLM
import json
import asyncio


app = FastAPI()


async def generate_stream(question: str, contexts: List[str]):
    """스트리밍 생성기"""
    # 1. 검색 결과 전송
    yield f"data: {json.dumps({'type': 'sources', 'data': contexts[:3]})}\n\n"

    # 2. 프롬프트 구성
    context_text = "\n".join(contexts)
    prompt = f"""컨텍스트:
{context_text}

질문: {question}
답변:"""

    # 3. LLM 스트리밍
    llm = OllamaLLM(model="llama4")

    for chunk in llm.stream(prompt):
        data = {"type": "token", "data": chunk}
        yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(0)  # 이벤트 루프 양보

    # 4. 완료 신호
    yield f"data: {json.dumps({'type': 'done'})}\n\n"


@app.get("/stream")
async def stream_response(question: str):
    """스트리밍 엔드포인트"""
    # 검색 (실제로는 벡터 검색)
    contexts = ["컨텍스트 1", "컨텍스트 2"]

    return StreamingResponse(
        generate_stream(question, contexts),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
