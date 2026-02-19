from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.documents import Document

# 문서 준비
documents = [
    Document(page_content="LangChain은 LLM 애플리케이션을 만드는 프레임워크입니다. 체인, 에이전트, 메모리 등의 개념을 제공합니다."),
    Document(page_content="RAG는 Retrieval-Augmented Generation의 약자입니다. 검색 결과를 활용하여 LLM의 답변을 개선합니다."),
    Document(page_content="벡터 데이터베이스는 임베딩 벡터를 저장하고 유사도 검색을 수행합니다."),
]

# 벡터 저장소
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(documents, embeddings)

# LLM
llm = OllamaLLM(model="llama4")

# RetrievalQA 체인
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# 질문
result = qa.invoke("LangChain이 뭐야?")
print(result["result"])
