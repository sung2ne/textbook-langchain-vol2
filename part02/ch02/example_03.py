from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

# 문서 준비
documents = [
    Document(
        page_content="파이썬은 배우기 쉬운 프로그래밍 언어입니다.",
        metadata={"source": "python_guide.txt", "chapter": 1}
    ),
    Document(
        page_content="LangChain은 LLM 애플리케이션을 만드는 프레임워크입니다.",
        metadata={"source": "langchain_docs.txt", "chapter": 1}
    ),
    Document(
        page_content="RAG는 검색 증강 생성으로, 외부 지식을 활용합니다.",
        metadata={"source": "rag_intro.txt", "chapter": 2}
    ),
]

# 문서에서 벡터 저장소 생성
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="knowledge_base"
)

print(f"문서 수: {vectorstore._collection.count()}")
