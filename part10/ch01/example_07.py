# FastAPI 스트리밍
from fastapi.responses import StreamingResponse

@app.get("/stream")
async def stream(question: str):
    return StreamingResponse(
        generate(question),
        media_type="text/event-stream"
    )
