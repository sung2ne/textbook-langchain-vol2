class LinkedChunker:
    """연결된 청킹"""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def split(self, documents: List[Document]) -> List[Document]:
        """연결 정보와 함께 분할"""
        all_chunks = []

        for doc in documents:
            chunks = self.splitter.split_text(doc.page_content)

            for i, chunk_content in enumerate(chunks):
                chunk = Document(
                    page_content=chunk_content,
                    metadata={
                        **doc.metadata,
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "has_prev": i > 0,
                        "has_next": i < len(chunks) - 1,
                        "prev_preview": chunks[i-1][-100:] if i > 0 else None,
                        "next_preview": chunks[i+1][:100] if i < len(chunks) - 1 else None
                    }
                )
                all_chunks.append(chunk)

        return all_chunks


# 사용
linked_chunker = LinkedChunker(chunk_size=200)
linked_chunks = linked_chunker.split(documents)

for chunk in linked_chunks[:2]:
    print(f"청크 {chunk.metadata['chunk_index']}/{chunk.metadata['total_chunks']}")
    print(f"이전: {chunk.metadata.get('has_prev')}")
    print(f"다음: {chunk.metadata.get('has_next')}")
    if chunk.metadata.get("next_preview"):
        print(f"다음 미리보기: {chunk.metadata['next_preview'][:30]}...")
    print()
