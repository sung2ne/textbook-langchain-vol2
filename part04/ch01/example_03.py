from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

# 벡터 저장소 준비
embeddings = OllamaEmbeddings(model="nomic-embed-text")
documents = [
    Document(page_content="RAG는 검색 증강 생성입니다."),
    Document(page_content="임베딩은 텍스트를 벡터로 변환합니다."),
    Document(page_content="벡터 DB는 유사도 검색을 수행합니다."),
]
vectorstore = Chroma.from_documents(documents, embeddings)

# MultiQueryRetriever
retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)

# 검색 (내부적으로 여러 쿼리 생성)
results = retriever.invoke("RAG 작동 원리")

for doc in results:
    print(f"- {doc.page_content}")
