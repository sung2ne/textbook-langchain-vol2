import re
from typing import List


def extract_sections(content: str) -> List[dict]:
    """마크다운에서 섹션 추출"""
    sections = []
    current_section = {"title": "Introduction", "level": 0, "content": []}

    for line in content.split("\n"):
        # 헤딩 찾기
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)

        if heading_match:
            # 이전 섹션 저장
            if current_section["content"]:
                current_section["content"] = "\n".join(current_section["content"])
                sections.append(current_section)

            # 새 섹션 시작
            level = len(heading_match.group(1))
            title = heading_match.group(2)
            current_section = {"title": title, "level": level, "content": []}
        else:
            current_section["content"].append(line)

    # 마지막 섹션 저장
    if current_section["content"]:
        current_section["content"] = "\n".join(current_section["content"])
        sections.append(current_section)

    return sections


def create_section_documents(content: str, base_metadata: dict = None) -> List[Document]:
    """섹션별 문서 생성"""
    sections = extract_sections(content)
    documents = []

    for i, section in enumerate(sections):
        metadata = base_metadata.copy() if base_metadata else {}
        metadata.update({
            "section_title": section["title"],
            "section_level": section["level"],
            "section_index": i
        })

        doc = Document(page_content=section["content"], metadata=metadata)
        documents.append(doc)

    return documents


# 사용
markdown_content = """
# LangChain 가이드

## 소개
LangChain은 LLM 프레임워크입니다.

## 설치
pip install langchain

### 의존성
Python 3.10 이상 필요합니다.

## 사용법
간단한 예제입니다.
"""

docs = create_section_documents(markdown_content, {"source": "guide.md"})

for doc in docs:
    print(f"[{doc.metadata['section_level']}] {doc.metadata['section_title']}")
    print(f"   {doc.page_content[:50]}...")
