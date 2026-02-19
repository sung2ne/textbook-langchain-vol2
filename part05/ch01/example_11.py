from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from typing import List, Dict, Optional
from datetime import datetime
import json


class MetadataEnrichedRAG:
    """메타데이터 강화 RAG 시스템"""

    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vectorstore = None
        self.metadata_index = MetadataIndex()

    def add_documents(self, documents: List[Document]):
        """문서 추가"""
        # 메타데이터 보강
        enriched_docs = []
        for i, doc in enumerate(documents):
            doc.metadata["doc_id"] = f"doc_{i}_{datetime.now().timestamp()}"
            doc.metadata["added_at"] = datetime.now().isoformat()
            doc.metadata["char_count"] = len(doc.page_content)

            enriched_docs.append(doc)
            self.metadata_index.add_document(doc.metadata["doc_id"], doc.metadata)

        # 벡터 저장소에 추가
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(enriched_docs, self.embeddings)
        else:
            self.vectorstore.add_documents(enriched_docs)

    def search(self, query: str, k: int = 5,
               metadata_filter: Optional[Dict] = None) -> List[Document]:
        """검색"""
        if self.vectorstore is None:
            return []

        return self.vectorstore.similarity_search(
            query,
            k=k,
            filter=metadata_filter
        )

    def search_by_metadata(self, **filters) -> List[str]:
        """메타데이터로만 검색"""
        return list(self.metadata_index.query(**filters))

    def get_metadata_stats(self) -> Dict:
        """메타데이터 통계"""
        stats = {}
        for field in ["level", "source", "category"]:
            values = self.metadata_index.get_unique_values(field)
            if values:
                stats[field] = {
                    "unique_count": len(values),
                    "values": values[:10]  # 상위 10개만
                }
        return stats


# 사용
rag = MetadataEnrichedRAG()

# 문서 추가
documents = [
    Document(
        page_content="LangChain 설치 방법입니다.",
        metadata={"source": "guide.md", "level": 2, "category": "installation"}
    ),
    Document(
        page_content="LangChain 기본 사용법입니다.",
        metadata={"source": "guide.md", "level": 2, "category": "usage"}
    ),
    Document(
        page_content="RAG 시스템 구축하기",
        metadata={"source": "tutorial.md", "level": 1, "category": "tutorial"}
    ),
]

rag.add_documents(documents)

# 검색
print("=== 일반 검색 ===")
results = rag.search("설치 방법")
for doc in results:
    print(f"- {doc.page_content[:30]}... [{doc.metadata.get('category')}]")

print("\n=== 필터 검색 ===")
results = rag.search("방법", metadata_filter={"category": "installation"})
for doc in results:
    print(f"- {doc.page_content[:30]}...")

print("\n=== 메타데이터 통계 ===")
print(json.dumps(rag.get_metadata_stats(), indent=2, ensure_ascii=False))
