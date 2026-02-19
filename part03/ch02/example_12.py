def get_splitter(document_type: str, chunk_size: int = 500):
    """문서 유형에 맞는 분할기 반환"""
    from langchain.text_splitter import (
        RecursiveCharacterTextSplitter,
        MarkdownTextSplitter,
        Language
    )

    if document_type == "markdown":
        return MarkdownTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=50
        )

    elif document_type == "code":
        return RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=chunk_size,
            chunk_overlap=50
        )

    elif document_type == "technical":
        # 기술 문서: 작은 청크
        return RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=30
        )

    else:
        # 기본
        return RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=int(chunk_size * 0.1)
        )


# 사용
splitter = get_splitter("markdown")
chunks = splitter.split_text(markdown_content)
