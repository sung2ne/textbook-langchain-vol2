qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="map_rerank",
    retriever=retriever
)
