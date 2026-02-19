from langchain_core.documents import Document
from langchain.document_loaders.base import BaseLoader
from typing import List
import os


class CustomTextLoader(BaseLoader):
    """커스텀 텍스트 로더"""

    def __init__(self, directory: str, encoding: str = "utf-8"):
        self.directory = directory
        self.encoding = encoding

    def load(self) -> List[Document]:
        documents = []

        for filename in os.listdir(self.directory):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.directory, filename)

                with open(filepath, "r", encoding=self.encoding) as f:
                    content = f.read()

                doc = Document(
                    page_content=content,
                    metadata={
                        "source": filepath,
                        "filename": filename,
                        "size": len(content)
                    }
                )
                documents.append(doc)

        return documents


# 사용
loader = CustomTextLoader("./my_documents")
documents = loader.load()
