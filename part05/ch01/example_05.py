from langchain_community.document_loaders import TextLoader
from pathlib import Path
import os
from datetime import datetime


def load_with_metadata(file_path: str) -> Document:
    """메타데이터와 함께 문서 로드"""
    loader = TextLoader(file_path, encoding="utf-8")
    docs = loader.load()

    # 파일 정보 추출
    path = Path(file_path)
    stat = os.stat(file_path)

    # 메타데이터 추가
    for doc in docs:
        doc.metadata.update({
            "filename": path.name,
            "extension": path.suffix,
            "directory": str(path.parent),
            "file_size": stat.st_size,
            "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        })

    return docs


# 사용
docs = load_with_metadata("./documents/guide.txt")
print(docs[0].metadata)
