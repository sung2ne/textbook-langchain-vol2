from abc import ABC, abstractmethod
from enum import Enum


class VectorStoreType(Enum):
    CHROMA = "chroma"
    FAISS = "faiss"
    QDRANT = "qdrant"


class VectorStoreFactory:
    """벡터 저장소 팩토리"""

    @staticmethod
    def create(store_type: VectorStoreType, embeddings, **kwargs):
        """벡터 저장소 생성"""

        if store_type == VectorStoreType.CHROMA:
            from langchain_community.vectorstores import Chroma
            return Chroma(
                embedding_function=embeddings,
                collection_name=kwargs.get("collection_name", "default"),
                persist_directory=kwargs.get("persist_directory")
            )

        elif store_type == VectorStoreType.FAISS:
            from langchain_community.vectorstores import FAISS
            # FAISS는 문서가 있어야 생성 가능
            if "documents" in kwargs:
                return FAISS.from_documents(kwargs["documents"], embeddings)
            elif "texts" in kwargs:
                return FAISS.from_texts(kwargs["texts"], embeddings)
            else:
                raise ValueError("FAISS requires documents or texts")

        elif store_type == VectorStoreType.QDRANT:
            from langchain_community.vectorstores import Qdrant
            return Qdrant.from_documents(
                kwargs.get("documents", []),
                embeddings,
                location=kwargs.get("location", ":memory:"),
                collection_name=kwargs.get("collection_name", "default")
            )

        else:
            raise ValueError(f"Unknown store type: {store_type}")

    @staticmethod
    def from_documents(store_type: VectorStoreType, documents, embeddings, **kwargs):
        """문서로부터 벡터 저장소 생성"""

        if store_type == VectorStoreType.CHROMA:
            from langchain_community.vectorstores import Chroma
            return Chroma.from_documents(
                documents,
                embeddings,
                collection_name=kwargs.get("collection_name", "default"),
                persist_directory=kwargs.get("persist_directory")
            )

        elif store_type == VectorStoreType.FAISS:
            from langchain_community.vectorstores import FAISS
            return FAISS.from_documents(documents, embeddings)

        elif store_type == VectorStoreType.QDRANT:
            from langchain_community.vectorstores import Qdrant
            return Qdrant.from_documents(
                documents,
                embeddings,
                location=kwargs.get("location", ":memory:"),
                collection_name=kwargs.get("collection_name", "default")
            )


# 사용 예시
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

embeddings = OllamaEmbeddings(model="nomic-embed-text")
documents = [
    Document(page_content="문서 1"),
    Document(page_content="문서 2"),
]

# ChromaDB 사용
chroma_store = VectorStoreFactory.from_documents(
    VectorStoreType.CHROMA,
    documents,
    embeddings,
    collection_name="test"
)

# FAISS로 전환
faiss_store = VectorStoreFactory.from_documents(
    VectorStoreType.FAISS,
    documents,
    embeddings
)

# 동일한 인터페이스로 검색
results1 = chroma_store.similarity_search("검색어")
results2 = faiss_store.similarity_search("검색어")
