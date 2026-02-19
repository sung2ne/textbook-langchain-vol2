from typing import Dict, List


class RAGASMetrics:
    """RAGAS 스타일 평가 지표"""

    def __init__(self):
        self.llm_evaluator = LLMEvaluator()

    def context_precision(self, question: str, contexts: List[str],
                         ground_truth: str) -> float:
        """컨텍스트 정밀도: 관련 컨텍스트가 상위에 있는지"""
        # 각 컨텍스트의 관련성 평가
        relevances = []

        for ctx in contexts:
            prompt = f"""이 컨텍스트가 질문에 답하는 데 필요한가요?

질문: {question}
정답: {ground_truth}
컨텍스트: {ctx[:500]}

"예" 또는 "아니오"로만 답하세요."""

            result = self.llm_evaluator.llm.invoke(prompt)
            relevances.append(1 if "예" in result else 0)

        # 가중 평균 (상위가 더 중요)
        if not relevances or sum(relevances) == 0:
            return 0.0

        weighted_sum = sum(
            rel * (1.0 / (i + 1))
            for i, rel in enumerate(relevances)
        )
        ideal_sum = sum(1.0 / (i + 1) for i in range(sum(relevances)))

        return weighted_sum / ideal_sum if ideal_sum > 0 else 0.0

    def context_recall(self, ground_truth: str, contexts: List[str]) -> float:
        """컨텍스트 재현율: 정답 정보가 컨텍스트에 있는지"""
        combined_context = "\n".join(contexts)

        prompt = f"""정답의 정보가 컨텍스트에 얼마나 포함되어 있는지 평가하세요.

정답:
{ground_truth}

컨텍스트:
{combined_context[:2000]}

0.0 ~ 1.0 사이의 숫자만 답하세요. (1.0 = 모든 정보 포함)"""

        result = self.llm_evaluator.llm.invoke(prompt)

        try:
            return float(result.strip())
        except ValueError:
            return 0.5

    def answer_similarity(self, answer: str, ground_truth: str) -> float:
        """답변 유사도"""
        prompt = f"""두 텍스트의 의미적 유사도를 평가하세요.

텍스트1: {answer}
텍스트2: {ground_truth}

0.0 ~ 1.0 사이의 숫자만 답하세요. (1.0 = 동일한 의미)"""

        result = self.llm_evaluator.llm.invoke(prompt)

        try:
            return float(result.strip())
        except ValueError:
            return 0.5


# 사용
ragas = RAGASMetrics()

question = "LangChain의 주요 컴포넌트는?"
contexts = [
    "LangChain은 LLM, 체인, 에이전트 컴포넌트로 구성됩니다.",
    "LangChain은 2022년에 출시되었습니다."
]
ground_truth = "LangChain의 주요 컴포넌트는 LLM, 체인, 에이전트입니다."

print(f"Context Precision: {ragas.context_precision(question, contexts, ground_truth):.2f}")
print(f"Context Recall: {ragas.context_recall(ground_truth, contexts):.2f}")
