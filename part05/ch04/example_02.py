from typing import List, Union
import numpy as np


class MultimodalEmbeddings:
    """멀티모달 임베딩 (CLIP 기반)"""

    def __init__(self):
        # CLIP 모델 로드 (실제로는 clip-as-service 사용)
        self.text_dim = 512
        self.image_dim = 512

    def embed_text(self, text: str) -> List[float]:
        """텍스트 임베딩"""
        # 실제로는 CLIP 텍스트 인코더 사용
        return [0.0] * self.text_dim

    def embed_image(self, image_path: str) -> List[float]:
        """이미지 임베딩"""
        # 실제로는 CLIP 이미지 인코더 사용
        return [0.0] * self.image_dim

    def embed_documents(self, items: List[dict]) -> List[List[float]]:
        """문서/이미지 임베딩"""
        embeddings = []

        for item in items:
            if item.get("type") == "image":
                emb = self.embed_image(item["path"])
            else:
                emb = self.embed_text(item["text"])
            embeddings.append(emb)

        return embeddings

    def similarity(self, query_emb: List[float], doc_emb: List[float]) -> float:
        """코사인 유사도"""
        q = np.array(query_emb)
        d = np.array(doc_emb)

        return float(np.dot(q, d) / (np.linalg.norm(q) * np.linalg.norm(d)))
