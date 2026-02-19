texts = [
    "파이썬은 배우기 쉽습니다.",
    "LangChain은 LLM 프레임워크입니다.",
    "RAG는 검색 증강 생성입니다.",
]

metadatas = [
    {"topic": "python"},
    {"topic": "langchain"},
    {"topic": "rag"},
]

vectorstore = Chroma.from_texts(
    texts=texts,
    embedding=embeddings,
    metadatas=metadatas,
    collection_name="simple_docs"
)
