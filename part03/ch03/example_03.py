from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

# 벡터 저장소 생성
embeddings = OllamaEmbeddings(model="nomic-embed-text")

documents = [
    Document(page_content="파이썬은 프로그래밍 언어입니다."),
    Document(page_content="LangChain은 LLM 프레임워크입니다."),
    Document(page_content="RAG는 검색 증강 생성입니다."),
    Document(page_content="벡터 DB는 임베딩을 저장합니다."),
]

vectorstore = Chroma.from_documents(documents, embeddings)

# Retriever로 변환
retriever = vectorstore.as_retriever()

# 검색
results = retriever.invoke("AI 개발 도구")

for doc in results:
    print(doc.page_content)
