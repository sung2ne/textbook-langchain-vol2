from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List, Dict
import uuid


class HierarchicalChunker:
    """계층적 청킹 시스템"""

    def __init__(self, parent_chunk_size: int = 2000,
                 child_chunk_size: int = 400,
                 chunk_overlap: int = 50):
        self.parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=parent_chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=child_chunk_size,
            chunk_overlap=chunk_overlap
        )

    def split(self, documents: List[Document]) -> Dict:
        """계층적 분할"""
        parent_docs = []
        child_docs = []
        parent_child_map = {}

        # 부모 청크 생성
        parent_chunks = self.parent_splitter.split_documents(documents)

        for parent in parent_chunks:
            parent_id = str(uuid.uuid4())
            parent.metadata["chunk_id"] = parent_id
            parent.metadata["chunk_type"] = "parent"
            parent_docs.append(parent)

            # 자식 청크 생성
            children = self.child_splitter.split_text(parent.page_content)
            child_ids = []

            for i, child_content in enumerate(children):
                child_id = f"{parent_id}_child_{i}"
                child_doc = Document(
                    page_content=child_content,
                    metadata={
                        **parent.metadata,
                        "chunk_id": child_id,
                        "chunk_type": "child",
                        "parent_id": parent_id,
                        "child_index": i
                    }
                )
                child_docs.append(child_doc)
                child_ids.append(child_id)

            parent_child_map[parent_id] = child_ids

        return {
            "parents": parent_docs,
            "children": child_docs,
            "mapping": parent_child_map
        }


# 사용
chunker = HierarchicalChunker(
    parent_chunk_size=1000,
    child_chunk_size=200
)

documents = [
    Document(page_content="""
LangChain은 대규모 언어 모델(LLM)을 활용한 애플리케이션을 개발하기 위한 프레임워크입니다.

LangChain의 주요 기능:
- 체인(Chains): 여러 LLM 호출을 연결
- 에이전트(Agents): 도구를 사용하는 자율적 LLM
- 메모리(Memory): 대화 기록 저장

설치 방법:
pip install langchain

간단한 예제:
from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="llama4")
result = llm.invoke("안녕하세요")
""", metadata={"source": "langchain_guide.md"})
]

result = chunker.split(documents)

print(f"부모 청크: {len(result['parents'])}개")
print(f"자식 청크: {len(result['children'])}개")

print("\n=== 부모 청크 ===")
for parent in result["parents"][:1]:
    print(f"ID: {parent.metadata['chunk_id'][:8]}...")
    print(f"길이: {len(parent.page_content)}자")

print("\n=== 자식 청크 ===")
for child in result["children"][:3]:
    print(f"ID: {child.metadata['chunk_id'][:20]}...")
    print(f"부모: {child.metadata['parent_id'][:8]}...")
    print(f"내용: {child.page_content[:50]}...")
    print()
