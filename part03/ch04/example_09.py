from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# 메모리
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

# 대화형 RAG
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True
)

# 대화
result1 = qa.invoke({"question": "LangChain이 뭐야?"})
print(f"A1: {result1['answer']}")

result2 = qa.invoke({"question": "그것의 주요 기능은?"})
print(f"A2: {result2['answer']}")  # "그것" = LangChain 이해
