from langchain_core.documents import Document
from typing import List, Tuple
import numpy as np


class CLIPImageSearch:
    """CLIP 기반 이미지 검색"""

    def __init__(self):
        self.embeddings = MultimodalEmbeddings()
        self.documents: List[Document] = []
        self.vectors: List[List[float]] = []

    def add_images(self, image_paths: List[str]):
        """이미지 추가"""
        for path in image_paths:
            doc = Document(
                page_content=f"이미지: {path}",
                metadata={"source": path, "type": "image"}
            )
            self.documents.append(doc)

            vector = self.embeddings.embed_image(path)
            self.vectors.append(vector)

    def add_texts(self, texts: List[str], sources: List[str] = None):
        """텍스트 추가"""
        for i, text in enumerate(texts):
            source = sources[i] if sources else f"text_{i}"
            doc = Document(
                page_content=text,
                metadata={"source": source, "type": "text"}
            )
            self.documents.append(doc)

            vector = self.embeddings.embed_text(text)
            self.vectors.append(vector)

    def search(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        """텍스트 쿼리로 검색"""
        query_vector = self.embeddings.embed_text(query)

        # 유사도 계산
        scores = []
        for i, doc_vector in enumerate(self.vectors):
            score = self.embeddings.similarity(query_vector, doc_vector)
            scores.append((i, score))

        # 상위 k개
        scores.sort(key=lambda x: x[1], reverse=True)
        top_k = scores[:k]

        results = [(self.documents[i], score) for i, score in top_k]
        return results

    def search_by_image(self, image_path: str, k: int = 5) -> List[Tuple[Document, float]]:
        """이미지로 유사 이미지/텍스트 검색"""
        query_vector = self.embeddings.embed_image(image_path)

        scores = []
        for i, doc_vector in enumerate(self.vectors):
            score = self.embeddings.similarity(query_vector, doc_vector)
            scores.append((i, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        top_k = scores[:k]

        results = [(self.documents[i], score) for i, score in top_k]
        return results


# 사용
search = CLIPImageSearch()

# 이미지와 텍스트 추가
# search.add_images(["cat.jpg", "dog.jpg", "car.jpg"])
# search.add_texts(["고양이 사진", "강아지 사진", "자동차 사진"])

# 텍스트로 검색
# results = search.search("귀여운 동물")
