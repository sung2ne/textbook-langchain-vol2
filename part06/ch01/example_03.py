from langchain_ollama import OllamaLLM
from typing import Dict


class LLMEvaluator:
    """LLM 기반 평가기"""

    def __init__(self, model: str = "llama4"):
        self.llm = OllamaLLM(model=model)

    def evaluate_faithfulness(self, answer: str, context: str) -> Dict:
        """충실도 평가"""
        prompt = f"""답변이 주어진 컨텍스트에 근거하는지 평가하세요.

컨텍스트:
{context}

답변:
{answer}

평가 기준:
- 답변의 모든 내용이 컨텍스트에서 확인 가능한가?
- 컨텍스트에 없는 정보를 추가했는가? (환각)

1-5점으로 평가하고 이유를 설명하세요.
형식: 점수: X/5, 이유: ...
"""

        result = self.llm.invoke(prompt)
        return {"raw_response": result, "metric": "faithfulness"}

    def evaluate_relevance(self, question: str, answer: str) -> Dict:
        """답변 관련성 평가"""
        prompt = f"""답변이 질문에 적절히 대답하는지 평가하세요.

질문:
{question}

답변:
{answer}

평가 기준:
- 질문의 핵심을 정확히 파악했는가?
- 질문에 대한 직접적인 답변인가?
- 불필요한 정보가 많지 않은가?

1-5점으로 평가하고 이유를 설명하세요.
형식: 점수: X/5, 이유: ...
"""

        result = self.llm.invoke(prompt)
        return {"raw_response": result, "metric": "relevance"}

    def evaluate_correctness(self, answer: str, ground_truth: str) -> Dict:
        """정확성 평가"""
        prompt = f"""생성된 답변과 정답을 비교하세요.

생성된 답변:
{answer}

정답:
{ground_truth}

평가 기준:
- 핵심 정보가 일치하는가?
- 사실적 오류가 있는가?
- 누락된 중요 정보가 있는가?

1-5점으로 평가하고 이유를 설명하세요.
형식: 점수: X/5, 이유: ...
"""

        result = self.llm.invoke(prompt)
        return {"raw_response": result, "metric": "correctness"}


# 사용
evaluator = LLMEvaluator()

context = "LangChain은 Harrison Chase가 2022년에 만든 LLM 프레임워크입니다."
question = "LangChain은 누가 만들었나요?"
answer = "LangChain은 Harrison Chase가 만들었습니다."

# 평가
faith_result = evaluator.evaluate_faithfulness(answer, context)
print(f"충실도 평가: {faith_result['raw_response']}")

rel_result = evaluator.evaluate_relevance(question, answer)
print(f"관련성 평가: {rel_result['raw_response']}")
