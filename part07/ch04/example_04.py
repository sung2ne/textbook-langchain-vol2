from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from langchain_ollama import OllamaLLM
import json


app = FastAPI()


class ConnectionManager:
    """WebSocket 연결 관리"""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket 채팅"""
    await manager.connect(websocket)

    try:
        while True:
            # 메시지 수신
            data = await websocket.receive_json()
            question = data.get("question", "")

            if not question:
                continue

            # 검색 결과 전송
            await manager.send_message(websocket, {
                "type": "sources",
                "data": ["검색 결과 1", "검색 결과 2"]
            })

            # LLM 스트리밍
            llm = OllamaLLM(model="llama4")

            for chunk in llm.stream(question):
                await manager.send_message(websocket, {
                    "type": "token",
                    "data": chunk
                })

            # 완료
            await manager.send_message(websocket, {
                "type": "done"
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
