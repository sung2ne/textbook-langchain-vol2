qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True  # 출처 반환
)

result = qa.invoke("RAG가 뭐야?")

print("답변:", result["result"])
print("\n출처 문서:")
for doc in result["source_documents"]:
    print(f"- {doc.page_content[:50]}...")
