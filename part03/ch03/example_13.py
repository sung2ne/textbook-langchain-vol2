from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 문서 저장소
docstore = InMemoryStore()

# 분할기
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200)
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)

# 문서 추가
retriever.add_documents(documents)

# 검색: 작은 청크로 매칭 → 큰 청크 반환
results = retriever.invoke("파이썬 설치")
