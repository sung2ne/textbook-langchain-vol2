import re
from typing import List, Dict
from langchain_core.documents import Document


def parse_markdown_table(table_text: str) -> List[Dict]:
    """마크다운 표 파싱"""
    lines = [line.strip() for line in table_text.strip().split("\n") if line.strip()]

    if len(lines) < 2:
        return []

    # 헤더 추출
    header_line = lines[0]
    headers = [h.strip() for h in header_line.split("|") if h.strip()]

    # 구분선 건너뛰기
    data_start = 1
    if re.match(r'^[\|\-\:\s]+$', lines[1]):
        data_start = 2

    # 데이터 추출
    rows = []
    for line in lines[data_start:]:
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if len(cells) == len(headers):
            row = dict(zip(headers, cells))
            rows.append(row)

    return rows


def table_to_documents(table_text: str, metadata: dict = None) -> List[Document]:
    """표를 행별 문서로 변환"""
    rows = parse_markdown_table(table_text)
    documents = []

    for i, row in enumerate(rows):
        # 행을 자연어로 변환
        content_parts = [f"{k}: {v}" for k, v in row.items()]
        content = ", ".join(content_parts)

        doc_metadata = metadata.copy() if metadata else {}
        doc_metadata.update({
            "type": "table_row",
            "row_index": i,
            "row_data": row
        })

        documents.append(Document(page_content=content, metadata=doc_metadata))

    return documents


# 사용
table_md = """
| 모델 | 차원 | 특징 |
|------|------|------|
| nomic-embed-text | 768 | 로컬, 무료 |
| all-MiniLM-L6-v2 | 384 | 가벼움, 빠름 |
| text-embedding-3-small | 1536 | 클라우드, 고품질 |
"""

docs = table_to_documents(table_md, {"source": "embedding_comparison.md"})

for doc in docs:
    print(f"행 {doc.metadata['row_index']}: {doc.page_content}")
