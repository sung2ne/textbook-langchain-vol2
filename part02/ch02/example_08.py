# 특정 토픽만 검색
results = vectorstore.similarity_search(
    "개발",
    k=3,
    filter={"topic": "langchain"}
)

# 복합 조건
results = vectorstore.similarity_search(
    "튜토리얼",
    k=3,
    filter={
        "$and": [
            {"chapter": {"$gte": 1}},
            {"source": {"$ne": "old.txt"}}
        ]
    }
)
