from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 스트리밍 LLM
streaming_llm = OllamaLLM(
    model="llama4",
    callbacks=[StreamingStdOutCallbackHandler()]
)

qa = RetrievalQA.from_chain_type(
    llm=streaming_llm,
    chain_type="stuff",
    retriever=retriever
)

# 스트리밍 실행
qa.invoke("RAG의 장점은?")
