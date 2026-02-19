from langchain.prompts import PromptTemplate

template = """다음 문맥을 사용하여 질문에 답하세요.
문맥에 답이 없으면 "정보가 없습니다"라고 말하세요.

문맥:
{context}

질문: {question}

답변:"""

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt}
)
