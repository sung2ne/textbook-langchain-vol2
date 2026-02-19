class HierarchicalDocumentProcessor:
    """계층적 문서 처리기"""

    def process(self, content: str, source: str) -> List[Document]:
        """계층 구조 유지하며 처리"""
        documents = []
        hierarchy = []  # [h1, h2, h3, ...]

        current_content = []
        current_heading = None

        for line in content.split("\n"):
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)

            if heading_match:
                # 이전 내용 저장
                if current_content and current_heading:
                    doc = self._create_document(
                        current_content, current_heading, hierarchy, source
                    )
                    documents.append(doc)

                # 계층 업데이트
                level = len(heading_match.group(1))
                title = heading_match.group(2)

                # 현재 레벨 이상 제거
                hierarchy = hierarchy[:level - 1]
                hierarchy.append(title)

                current_heading = {"title": title, "level": level}
                current_content = []
            else:
                current_content.append(line)

        # 마지막 섹션
        if current_content and current_heading:
            doc = self._create_document(
                current_content, current_heading, hierarchy, source
            )
            documents.append(doc)

        return documents

    def _create_document(self, content, heading, hierarchy, source):
        """문서 생성"""
        return Document(
            page_content="\n".join(content).strip(),
            metadata={
                "source": source,
                "title": heading["title"],
                "level": heading["level"],
                "hierarchy": " > ".join(hierarchy),
                "parent": hierarchy[-2] if len(hierarchy) > 1 else None
            }
        )


# 사용
processor = HierarchicalDocumentProcessor()
docs = processor.process(markdown_content, "guide.md")

for doc in docs:
    print(f"계층: {doc.metadata['hierarchy']}")
    print(f"부모: {doc.metadata.get('parent', 'None')}")
    print()
