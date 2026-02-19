import json
from langchain_core.documents import Document


def load_json_documents(file_path, content_key="content"):
    """JSON 파일에서 문서 로드"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []
    for item in data:
        doc = Document(
            page_content=item.get(content_key, ""),
            metadata={k: v for k, v in item.items() if k != content_key}
        )
        documents.append(doc)

    return documents


# 사용
documents = load_json_documents("./data/articles.json", content_key="body")
