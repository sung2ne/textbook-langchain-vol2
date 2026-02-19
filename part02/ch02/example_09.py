from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 영속적 저장소 생성
vectorstore = Chroma(
    collection_name="persistent_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db"  # 저장 경로
)

# 문서 추가
vectorstore.add_texts(
    texts=["저장될 문서입니다."],
    metadatas=[{"saved": True}]
)

print("데이터 저장 완료")
