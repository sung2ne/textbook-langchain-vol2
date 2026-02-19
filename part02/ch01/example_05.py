# 특정 카테고리만 검색
results = collection.query(
    query_texts=["웹 개발"],
    where={"category": "programming"},
    n_results=5
)

# 복합 조건
results = collection.query(
    query_texts=["튜토리얼"],
    where={
        "$and": [
            {"category": "programming"},
            {"lang": "python"}
        ]
    },
    n_results=5
)

# 비교 연산자
results = collection.query(
    query_texts=["최신 문서"],
    where={"year": {"$gte": 2023}},  # 2023년 이상
    n_results=5
)
