from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from typing import List, Dict, Tuple
import uuid


class HierarchicalRAG:
    """계층적 RAG 시스템"""

    def __init__(self, parent_size: int = 1000, child_size: int = 200):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.parent_size = parent_size
        self.child_size = child_size

        self.parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=parent_size,
            chunk_overlap=parent_size // 10
        )
        self.child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=child_size,
            chunk_overlap=child_size // 10
        )

        self.vectorstore = None
        self.parent_store = {}  # parent_id -> Document

    def add_documents(self, documents: List[Document]):
        """문서 추가"""
        child_docs = []

        for doc in documents:
            # 부모 청크 생성
            parent_chunks = self.parent_splitter.split_text(doc.page_content)

            for p_idx, parent_content in enumerate(parent_chunks):
                parent_id = str(uuid.uuid4())

                # 부모 저장
                parent_doc = Document(
                    page_content=parent_content,
                    metadata={
                        **doc.metadata,
                        "chunk_id": parent_id,
                        "chunk_type": "parent"
                    }
                )
                self.parent_store[parent_id] = parent_doc

                # 자식 청크 생성
                child_chunks = self.child_splitter.split_text(parent_content)

                for c_idx, child_content in enumerate(child_chunks):
                    child_doc = Document(
                        page_content=child_content,
                        metadata={
                            **doc.metadata,
                            "parent_id": parent_id,
                            "chunk_type": "child",
                            "child_index": c_idx
                        }
                    )
                    child_docs.append(child_doc)

        # 자식만 벡터 저장소에
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(child_docs, self.embeddings)
        else:
            self.vectorstore.add_documents(child_docs)

        print(f"부모: {len(self.parent_store)}개, 자식: {len(child_docs)}개 추가")

    def search(self, query: str, k: int = 3,
               return_type: str = "parent") -> List[Document]:
        """검색

        return_type: "child", "parent", "both"
        """
        if self.vectorstore is None:
            return []

        # 자식 청크 검색
        child_results = self.vectorstore.similarity_search(query, k=k * 2)

        if return_type == "child":
            return child_results[:k]

        # 부모 청크 수집 (중복 제거)
        seen_parents = set()
        parent_results = []

        for child in child_results:
            parent_id = child.metadata.get("parent_id")
            if parent_id and parent_id not in seen_parents:
                seen_parents.add(parent_id)
                if parent_id in self.parent_store:
                    parent_results.append(self.parent_store[parent_id])

            if len(parent_results) >= k:
                break

        if return_type == "parent":
            return parent_results

        # both: 부모와 매칭된 자식 함께 반환
        return [(parent, [c for c in child_results if c.metadata.get("parent_id") == parent.metadata.get("chunk_id")])
                for parent in parent_results]

    def search_with_context(self, query: str, k: int = 3) -> List[Dict]:
        """문맥과 함께 검색"""
        child_results = self.vectorstore.similarity_search_with_score(query, k=k * 2)

        results = []
        seen_parents = set()

        for child, score in child_results:
            parent_id = child.metadata.get("parent_id")
            if parent_id in seen_parents:
                continue

            seen_parents.add(parent_id)
            parent = self.parent_store.get(parent_id)

            results.append({
                "matched_chunk": child.page_content,
                "full_context": parent.page_content if parent else None,
                "score": score,
                "metadata": child.metadata
            })

            if len(results) >= k:
                break

        return results


# 사용
rag = HierarchicalRAG(parent_size=800, child_size=150)

documents = [
    Document(
        page_content="""
LangChain은 대규모 언어 모델(LLM)을 활용한 애플리케이션을 개발하기 위한 프레임워크입니다.
체인, 에이전트, 메모리 등의 개념을 제공합니다.

체인(Chains)은 여러 LLM 호출을 연결하여 복잡한 작업을 수행합니다.
예를 들어, 문서 요약 후 번역하는 체인을 만들 수 있습니다.

에이전트(Agents)는 도구를 사용하는 자율적인 LLM입니다.
웹 검색, 계산기, 데이터베이스 조회 등의 도구를 활용합니다.

메모리(Memory)는 대화 기록을 저장하고 관리합니다.
이전 대화 내용을 기억하여 문맥에 맞는 응답을 생성합니다.
""",
        metadata={"source": "langchain_guide.md"}
    )
]

rag.add_documents(documents)

# 검색 테스트
print("\n=== 자식 청크 검색 ===")
results = rag.search("에이전트 도구", k=2, return_type="child")
for doc in results:
    print(f"- {doc.page_content[:60]}...")

print("\n=== 부모 청크 검색 ===")
results = rag.search("에이전트 도구", k=1, return_type="parent")
for doc in results:
    print(f"길이: {len(doc.page_content)}자")
    print(f"내용: {doc.page_content[:100]}...")

print("\n=== 문맥과 함께 검색 ===")
results = rag.search_with_context("에이전트 도구", k=1)
for r in results:
    print(f"매칭: {r['matched_chunk'][:50]}...")
    print(f"점수: {r['score']:.4f}")
    print(f"전체 문맥 길이: {len(r['full_context'])}자")
