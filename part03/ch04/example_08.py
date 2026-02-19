from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser


def format_docs(docs):
    """문서 포맷팅"""
    return "\n\n".join(doc.page_content for doc in docs)


# 프롬프트
prompt = ChatPromptTemplate.from_template("""
다음 문맥을 바탕으로 질문에 답하세요.

문맥:
{context}

질문: {question}

답변:""")

# LCEL 체인
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# 실행
answer = rag_chain.invoke("LangChain이 뭐야?")
print(answer)
