# 필터로 검색
results = vectorstore.similarity_search(
    "정보",
    k=5,
    filter={"category": "tech"}
)

# 필터 함수 사용
def my_filter(metadata):
    return metadata.get("category") == "weather"

results = vectorstore.similarity_search(
    "오늘",
    k=5,
    filter=my_filter
)
