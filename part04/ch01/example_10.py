from enum import Enum
from typing import List


class QueryTransformationType(Enum):
    REWRITE = "rewrite"
    EXPAND = "expand"
    HYDE = "hyde"
    STEP_BACK = "step_back"
    DECOMPOSE = "decompose"


class QueryTransformer:
    """통합 쿼리 변환 시스템"""

    def __init__(self, llm):
        self.llm = llm

    def transform(self, question: str,
                  transformation_type: QueryTransformationType) -> List[str]:
        """질문 변환"""
        if transformation_type == QueryTransformationType.REWRITE:
            return [self._rewrite(question)]

        elif transformation_type == QueryTransformationType.EXPAND:
            return self._expand(question)

        elif transformation_type == QueryTransformationType.HYDE:
            return [self._hyde(question)]

        elif transformation_type == QueryTransformationType.STEP_BACK:
            return [question, self._step_back(question)]

        elif transformation_type == QueryTransformationType.DECOMPOSE:
            return self._decompose(question)

        return [question]

    def _rewrite(self, question: str) -> str:
        prompt = PromptTemplate(
            template="질문을 검색에 적합하게 재작성: {question}\n재작성:",
            input_variables=["question"]
        )
        return (prompt | self.llm).invoke({"question": question}).strip()

    def _expand(self, question: str) -> List[str]:
        prompt = PromptTemplate(
            template="다음 질문을 3개의 다른 표현으로 확장 (줄바꿈으로 구분): {question}\n확장:",
            input_variables=["question"]
        )
        result = (prompt | self.llm).invoke({"question": question})
        return [q.strip() for q in result.strip().split("\n") if q.strip()][:3]

    def _hyde(self, question: str) -> str:
        prompt = PromptTemplate(
            template="다음 질문에 대한 가상의 답변 (키워드 포함): {question}\n답변:",
            input_variables=["question"]
        )
        return (prompt | self.llm).invoke({"question": question}).strip()

    def _step_back(self, question: str) -> str:
        prompt = PromptTemplate(
            template="구체적 질문을 일반적으로 변환: {question}\n일반적 질문:",
            input_variables=["question"]
        )
        return (prompt | self.llm).invoke({"question": question}).strip()

    def _decompose(self, question: str) -> List[str]:
        prompt = PromptTemplate(
            template="복잡한 질문을 3개의 하위 질문으로 분해 (줄바꿈 구분): {question}\n하위 질문:",
            input_variables=["question"]
        )
        result = (prompt | self.llm).invoke({"question": question})
        return [q.strip().lstrip("0123456789.-) ")
                for q in result.strip().split("\n") if q.strip()][:3]


# 사용
transformer = QueryTransformer(llm)

question = "RAG 시스템 구축에 필요한 것들"

print("=== 쿼리 변환 테스트 ===\n")
print(f"원본: {question}\n")

for t_type in QueryTransformationType:
    print(f"--- {t_type.value} ---")
    results = transformer.transform(question, t_type)
    for r in results:
        print(f"  • {r}")
    print()
