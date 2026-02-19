from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_with_metadata(documents, chunk_size=500, chunk_overlap=50):
    """메타데이터를 유지하며 분할"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    split_docs = splitter.split_documents(documents)

    # 청크 인덱스 추가
    current_source = None
    chunk_index = 0

    for doc in split_docs:
        source = doc.metadata.get("source", "")

        if source != current_source:
            current_source = source
            chunk_index = 0

        doc.metadata["chunk_index"] = chunk_index
        doc.metadata["chunk_size"] = len(doc.page_content)
        chunk_index += 1

    return split_docs


# 사용
split_docs = split_with_metadata(docs)

for doc in split_docs[:3]:
    print(f"청크 {doc.metadata['chunk_index']}: {len(doc.page_content)}자")
