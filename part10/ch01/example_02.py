from langchain_community.vectorstores import Chroma

# 벡터 저장소 생성
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
