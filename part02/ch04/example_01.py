from langchain_community.vectorstores import Qdrant
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

embeddings = OllamaEmbeddings(model="nomic-embed-text")

documents = [
    Document(page_content="파이썬 프로그래밍", metadata={"topic": "python"}),
    Document(page_content="LangChain 프레임워크", metadata={"topic": "langchain"}),
]

# 메모리 모드
vectorstore = Qdrant.from_documents(
    documents,
    embeddings,
    location=":memory:",
    collection_name="test"
)

# 서버 모드
vectorstore = Qdrant.from_documents(
    documents,
    embeddings,
    url="http://localhost:6333",
    collection_name="my_docs"
)

# 검색
results = vectorstore.similarity_search("AI 도구", k=2)
