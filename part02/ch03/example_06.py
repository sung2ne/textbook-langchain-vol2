from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

# 임베딩 모델
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 문서 준비
documents = [
    Document(page_content="파이썬은 프로그래밍 언어입니다."),
    Document(page_content="LangChain은 LLM 프레임워크입니다."),
    Document(page_content="FAISS는 벡터 검색 라이브러리입니다."),
]

# FAISS 벡터 저장소 생성
vectorstore = FAISS.from_documents(documents, embeddings)

# 검색
results = vectorstore.similarity_search("AI 도구", k=2)
for doc in results:
    print(doc.page_content)
