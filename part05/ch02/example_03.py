import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Section:
    title: str
    level: int
    content: str
    children: List["Section"]
    parent: Optional["Section"] = None


class SectionParser:
    """섹션 기반 파서"""

    def parse(self, content: str) -> Section:
        """마크다운 섹션 파싱"""
        root = Section(title="root", level=0, content="", children=[])
        stack = [root]

        lines = content.split("\n")
        current_content = []

        for line in lines:
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)

            if heading_match:
                # 이전 내용 저장
                if current_content:
                    stack[-1].content += "\n".join(current_content)
                    current_content = []

                level = len(heading_match.group(1))
                title = heading_match.group(2)

                # 적절한 부모 찾기
                while len(stack) > 1 and stack[-1].level >= level:
                    stack.pop()

                section = Section(
                    title=title,
                    level=level,
                    content="",
                    children=[],
                    parent=stack[-1]
                )
                stack[-1].children.append(section)
                stack.append(section)
            else:
                current_content.append(line)

        # 마지막 내용
        if current_content:
            stack[-1].content += "\n".join(current_content)

        return root

    def to_documents(self, section: Section, include_hierarchy: bool = True) -> List[Document]:
        """섹션을 문서로 변환"""
        documents = []
        self._section_to_docs(section, documents, [], include_hierarchy)
        return documents

    def _section_to_docs(self, section: Section, documents: List[Document],
                         path: List[str], include_hierarchy: bool):
        """재귀적 문서 변환"""
        if section.title != "root":
            current_path = path + [section.title]

            metadata = {
                "title": section.title,
                "level": section.level,
            }

            if include_hierarchy:
                metadata["hierarchy"] = " > ".join(current_path)
                metadata["parent_title"] = path[-1] if path else None

            if section.content.strip():
                documents.append(Document(
                    page_content=section.content.strip(),
                    metadata=metadata
                ))
        else:
            current_path = path

        for child in section.children:
            self._section_to_docs(child, documents, current_path, include_hierarchy)


# 사용
parser = SectionParser()

markdown = """
# LangChain 가이드

## 소개
LangChain은 LLM 프레임워크입니다.

### 주요 기능
체인, 에이전트, 메모리를 제공합니다.

## 설치
pip install langchain

### 요구사항
Python 3.10 이상이 필요합니다.
"""

root = parser.parse(markdown)
docs = parser.to_documents(root)

for doc in docs:
    print(f"[{doc.metadata.get('level', 0)}] {doc.metadata.get('title', 'N/A')}")
    print(f"   계층: {doc.metadata.get('hierarchy', 'N/A')}")
    print(f"   내용: {doc.page_content[:30]}...")
    print()
