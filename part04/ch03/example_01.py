from sentence_transformers import CrossEncoder
from langchain_core.documents import Document
from typing import List, Tuple


class CrossEncoderReranker:
    """Cross-Encoder 기반 리랭커"""

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, documents: List[Document],
               top_k: int = 5) -> List[Tuple[Document, float]]:
        """문서 리랭킹"""
        if not documents:
            return []

        # 질문-문서 쌍 생성
        pairs = [[query, doc.page_content] for doc in documents]

        # 점수 계산
        scores = self.model.predict(pairs)

        # 점수와 문서 결합
        doc_scores = list(zip(documents, scores))

        # 점수순 정렬
        doc_scores.sort(key=lambda x: x[1], reverse=True)

        return doc_scores[:top_k]


# 사용
reranker = CrossEncoderReranker()

documents = [
    Document(page_content="Python은 프로그래밍 언어입니다."),
    Document(page_content="LangChain은 LLM 프레임워크입니다."),
    Document(page_content="오늘 날씨가 좋습니다."),
    Document(page_content="파이썬으로 AI 앱을 만듭니다."),
]

query = "Python으로 AI 개발하기"

reranked = reranker.rerank(query, documents, top_k=3)

print(f"질문: {query}\n")
print("리랭킹 결과:")
for doc, score in reranked:
    print(f"[{score:.4f}] {doc.page_content}")
