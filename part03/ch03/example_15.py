from langchain.schema.runnable import RunnablePassthrough


def create_filtered_retriever(vectorstore, category):
    """카테고리별 필터 Retriever"""
    return vectorstore.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"category": category}
        }
    )


# 카테고리별 Retriever
tutorial_retriever = create_filtered_retriever(vectorstore, "tutorial")
reference_retriever = create_filtered_retriever(vectorstore, "reference")

# 병렬 검색 후 결합
def combined_search(query):
    tutorial_results = tutorial_retriever.invoke(query)
    reference_results = reference_retriever.invoke(query)
    return tutorial_results + reference_results


results = combined_search("파이썬 함수")
