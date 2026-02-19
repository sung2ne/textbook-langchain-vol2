from fastapi import FastAPI, BackgroundTasks
from typing import Dict
import asyncio


app = FastAPI()

# 작업 상태 저장
task_status: Dict[str, Dict] = {}


async def process_documents_async(task_id: str, documents: list):
    """비동기 문서 처리"""
    task_status[task_id] = {"status": "processing", "progress": 0}

    for i, doc in enumerate(documents):
        # 처리 시뮬레이션
        await asyncio.sleep(0.1)
        task_status[task_id]["progress"] = (i + 1) / len(documents) * 100

    task_status[task_id] = {"status": "completed", "progress": 100}


@app.post("/documents/process-async")
async def process_async(background_tasks: BackgroundTasks):
    """비동기 문서 처리 시작"""
    import uuid

    task_id = str(uuid.uuid4())
    documents = rag_service.documents  # 예시

    # 백그라운드 작업 추가
    background_tasks.add_task(process_documents_async, task_id, documents)

    return {"task_id": task_id, "status": "started"}


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """작업 상태 조회"""
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_status[task_id]
