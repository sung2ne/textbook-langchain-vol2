from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings


def create_parent_retriever(documents: List[Document]):
    """ParentDocumentRetriever 생성"""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # 벡터 저장소 (자식 청크용)
    vectorstore = Chroma(
        collection_name="children",
        embedding_function=embeddings
    )

    # 문서 저장소 (부모 청크용)
    docstore = InMemoryStore()

    # 분할기
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=200)

    # Retriever 생성
    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=docstore,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter
    )

    # 문서 추가
    retriever.add_documents(documents)

    return retriever


# 사용
retriever = create_parent_retriever(documents)

# 검색 (자식으로 매칭 → 부모 반환)
results = retriever.invoke("LangChain 설치")

print("검색 결과 (부모 청크):")
for doc in results:
    print(f"길이: {len(doc.page_content)}자")
    print(f"내용: {doc.page_content[:100]}...")
