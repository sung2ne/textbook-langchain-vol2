from pathlib import Path
from typing import List, Union
import re


class UnifiedDocumentProcessor:
    """통합 문서 처리기"""

    def __init__(self):
        self.table_pattern = re.compile(r'\|.+\|[\s\n]+\|[\-\:]+\|[\s\n]+(\|.+\|[\s\n]*)+')

    def process(self, content: str, source: str = None) -> List[Document]:
        """문서 처리"""
        documents = []
        metadata = {"source": source} if source else {}

        # 표 추출 및 처리
        tables = self.table_pattern.findall(content)
        for i, table in enumerate(self.table_pattern.finditer(content)):
            table_docs = table_to_documents(table.group(), {
                **metadata,
                "table_index": i
            })
            documents.extend(table_docs)

        # 표를 제외한 텍스트 처리
        text_content = self.table_pattern.sub("[TABLE]", content)
        text_parts = [p.strip() for p in text_content.split("[TABLE]") if p.strip()]

        for i, text in enumerate(text_parts):
            documents.append(Document(
                page_content=text,
                metadata={**metadata, "type": "text", "segment": i}
            ))

        return documents


# 사용
processor = UnifiedDocumentProcessor()

mixed_content = """
# 임베딩 모델 비교

다양한 임베딩 모델을 비교합니다.

| 모델 | 차원 | 특징 |
|------|------|------|
| nomic | 768 | 로컬 |
| MiniLM | 384 | 빠름 |

위 표에서 보듯이 각 모델은 특성이 다릅니다.
"""

docs = processor.process(mixed_content, "comparison.md")

for doc in docs:
    print(f"타입: {doc.metadata.get('type', 'unknown')}")
    print(f"내용: {doc.page_content[:50]}...")
    print()
