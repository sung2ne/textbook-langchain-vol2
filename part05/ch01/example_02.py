# 특정 카테고리만 검색
results = vectorstore.similarity_search(
    "검색어",
    filter={"category": "tutorial"}
)
