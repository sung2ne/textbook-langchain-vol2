# 특정 조건의 문서만 검색
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5,
        "filter": {"category": "tutorial"}
    }
)

# 복합 조건
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5,
        "filter": {
            "$and": [
                {"category": "tutorial"},
                {"year": {"$gte": 2023}}
            ]
        }
    }
)
