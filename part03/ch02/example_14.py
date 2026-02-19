from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List


class DocumentProcessor:
    """문서 처리 파이프라인"""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

    def process(self, documents: List[Document]) -> List[Document]:
        """문서 처리 및 분할"""
        # 전처리
        cleaned_docs = self._clean_documents(documents)

        # 분할
        split_docs = self.splitter.split_documents(cleaned_docs)

        # 후처리
        final_docs = self._post_process(split_docs)

        return final_docs

    def _clean_documents(self, documents: List[Document]) -> List[Document]:
        """문서 정제"""
        cleaned = []
        for doc in documents:
            # 공백 정리
            content = " ".join(doc.page_content.split())
            # 빈 문서 제외
            if content.strip():
                cleaned.append(Document(
                    page_content=content,
                    metadata=doc.metadata
                ))
        return cleaned

    def _post_process(self, documents: List[Document]) -> List[Document]:
        """후처리"""
        processed = []
        for i, doc in enumerate(documents):
            # 청크 인덱스 추가
            doc.metadata["chunk_index"] = i
            doc.metadata["chunk_length"] = len(doc.page_content)
            processed.append(doc)
        return processed


# 사용
processor = DocumentProcessor(chunk_size=400, chunk_overlap=40)

# 샘플 문서
documents = [
    Document(
        page_content="""파이썬은 1991년 귀도 반 로섬이 발표한 프로그래밍 언어입니다.

        파이썬의 주요 특징은 다음과 같습니다:
        - 간결하고 읽기 쉬운 문법
        - 동적 타이핑
        - 풍부한 표준 라이브러리

        파이썬은 데이터 과학, 웹 개발, 인공지능 등 다양한 분야에서 사용됩니다.""",
        metadata={"source": "python_intro.txt"}
    )
]

processed_docs = processor.process(documents)

print(f"처리 결과: {len(processed_docs)}개 청크")
for doc in processed_docs:
    print(f"\n[청크 {doc.metadata['chunk_index']}] ({doc.metadata['chunk_length']}자)")
    print(doc.page_content[:100] + "...")
