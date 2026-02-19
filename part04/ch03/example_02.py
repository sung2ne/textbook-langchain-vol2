from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate


class LLMReranker:
    """LLM 기반 리랭커"""

    def __init__(self, llm=None):
        self.llm = llm or OllamaLLM(model="llama4")

        self.prompt = PromptTemplate(
            template="""다음 문서가 질문에 얼마나 관련있는지 1-10 점수로 평가하세요.
점수만 숫자로 답하세요.

질문: {query}

문서: {document}

점수:""",
            input_variables=["query", "document"]
        )

    def _score_document(self, query: str, document: str) -> float:
        """단일 문서 점수 계산"""
        chain = self.prompt | self.llm

        try:
            result = chain.invoke({"query": query, "document": document})
            # 숫자 추출
            score = float("".join(c for c in result if c.isdigit() or c == "."))
            return min(max(score, 1), 10) / 10  # 0-1 정규화
        except:
            return 0.5

    def rerank(self, query: str, documents: List[Document],
               top_k: int = 5) -> List[Tuple[Document, float]]:
        """문서 리랭킹"""
        doc_scores = []

        for doc in documents:
            score = self._score_document(query, doc.page_content)
            doc_scores.append((doc, score))

        # 정렬
        doc_scores.sort(key=lambda x: x[1], reverse=True)

        return doc_scores[:top_k]


# 사용
llm_reranker = LLMReranker()

reranked = llm_reranker.rerank(query, documents, top_k=3)

print("LLM 리랭킹 결과:")
for doc, score in reranked:
    print(f"[{score:.2f}] {doc.page_content}")
