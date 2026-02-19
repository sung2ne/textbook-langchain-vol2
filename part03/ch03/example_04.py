# 상위 5개 문서
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)
