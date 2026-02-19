from langchain_core.documents import Document
from typing import Iterator


def lazy_load_large_file(file_path: str, chunk_size: int = 1000) -> Iterator[Document]:
    """대용량 파일을 청크 단위로 로드"""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = []
        line_count = 0

        for line in f:
            lines.append(line)
            line_count += 1

            if line_count >= chunk_size:
                yield Document(
                    page_content="".join(lines),
                    metadata={"source": file_path, "chunk": line_count // chunk_size}
                )
                lines = []

        # 남은 라인 처리
        if lines:
            yield Document(
                page_content="".join(lines),
                metadata={"source": file_path, "chunk": "last"}
            )


# 사용 (메모리 효율적)
for doc in lazy_load_large_file("./large_file.txt", chunk_size=500):
    # 각 청크 처리
    print(f"청크: {doc.metadata['chunk']}, 길이: {len(doc.page_content)}")
