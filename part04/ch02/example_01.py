from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

# 문서 준비
documents = [
    Document(page_content="Python은 프로그래밍 언어입니다.", metadata={"id": 1}),
    Document(page_content="파이썬으로 웹 개발을 합니다.", metadata={"id": 2}),
    Document(page_content="LangChain은 LLM 프레임워크입니다.", metadata={"id": 3}),
    Document(page_content="RAG는 검색 증강 생성입니다.", metadata={"id": 4}),
]

# BM25 검색기 생성
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 3  # 상위 3개 반환

# 검색
results = bm25_retriever.invoke("Python 프로그래밍")

for doc in results:
    print(f"- {doc.page_content}")
