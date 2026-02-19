from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM

# RAG 체인
qa_chain = RetrievalQA.from_chain_type(
    llm=OllamaLLM(model="llama4"),
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

result = qa_chain.invoke({"query": "질문"})
