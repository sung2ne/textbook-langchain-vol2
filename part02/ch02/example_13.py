from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain_core.documents import Document


def create_qa_system(documents, persist_dir="./qa_db"):
    """문서 QA 시스템 생성"""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # 벡터 저장소 생성
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    # Retriever 생성
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3}
    )

    # LLM
    llm = OllamaLLM(model="llama4")

    # QA 체인
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain


# 샘플 문서
documents = [
    Document(
        page_content="""LangChain은 대규모 언어 모델(LLM)을 활용한 애플리케이션을
        개발하기 위한 프레임워크입니다. 체인, 에이전트, 메모리 등의 개념을 제공합니다.""",
        metadata={"source": "langchain_intro"}
    ),
    Document(
        page_content="""RAG(Retrieval-Augmented Generation)는 검색과 생성을 결합한
        기술입니다. 외부 지식 베이스에서 관련 정보를 검색하여 LLM의 응답을 개선합니다.""",
        metadata={"source": "rag_overview"}
    ),
    Document(
        page_content="""ChromaDB는 오픈소스 벡터 데이터베이스입니다.
        임베딩을 저장하고 유사도 검색을 수행할 수 있습니다.""",
        metadata={"source": "chromadb_docs"}
    ),
]

# QA 시스템 생성
qa = create_qa_system(documents)

# 질문
questions = [
    "LangChain이 뭐야?",
    "RAG가 어떻게 작동해?",
    "벡터 데이터베이스는 뭘 저장해?",
]

for q in questions:
    print(f"Q: {q}")
    result = qa.invoke(q)
    print(f"A: {result['result']}\n")
    print("참조 문서:")
    for doc in result["source_documents"]:
        print(f"  - {doc.metadata.get('source', 'unknown')}")
    print("-" * 50)
