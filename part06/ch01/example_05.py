from typing import Dict, List
from dataclasses import dataclass
import json


@dataclass
class EvaluationResult:
    """평가 결과"""
    question: str
    answer: str
    ground_truth: str
    contexts: List[str]
    metrics: Dict[str, float]


class RAGEvaluator:
    """통합 RAG 평가기"""

    def __init__(self):
        self.retrieval_metrics = RetrievalMetrics()
        self.llm_evaluator = LLMEvaluator()

    def evaluate(self, question: str, answer: str, ground_truth: str,
                retrieved_docs: List[str], relevant_docs: List[str],
                contexts: List[str]) -> EvaluationResult:
        """전체 평가"""

        # 검색 평가
        precision = self.retrieval_metrics.precision_at_k(retrieved_docs, relevant_docs, 5)
        recall = self.retrieval_metrics.recall_at_k(retrieved_docs, relevant_docs, 5)
        mrr = self.retrieval_metrics.mrr(retrieved_docs, relevant_docs)

        # 생성 평가 (LLM 기반)
        faith_result = self.llm_evaluator.evaluate_faithfulness(
            answer, "\n".join(contexts)
        )
        rel_result = self.llm_evaluator.evaluate_relevance(question, answer)
        correct_result = self.llm_evaluator.evaluate_correctness(answer, ground_truth)

        # 점수 추출 (간단한 파싱)
        def extract_score(result: Dict) -> float:
            text = result.get("raw_response", "")
            for i in range(5, 0, -1):
                if f"{i}/5" in text:
                    return i / 5.0
            return 0.5

        metrics = {
            "precision@5": precision,
            "recall@5": recall,
            "mrr": mrr,
            "faithfulness": extract_score(faith_result),
            "relevance": extract_score(rel_result),
            "correctness": extract_score(correct_result)
        }

        return EvaluationResult(
            question=question,
            answer=answer,
            ground_truth=ground_truth,
            contexts=contexts,
            metrics=metrics
        )

    def evaluate_batch(self, test_cases: List[Dict]) -> Dict:
        """배치 평가"""
        results = []

        for case in test_cases:
            result = self.evaluate(
                question=case["question"],
                answer=case["answer"],
                ground_truth=case["ground_truth"],
                retrieved_docs=case["retrieved_docs"],
                relevant_docs=case["relevant_docs"],
                contexts=case["contexts"]
            )
            results.append(result)

        # 평균 계산
        avg_metrics = {}
        metric_keys = results[0].metrics.keys() if results else []

        for key in metric_keys:
            values = [r.metrics[key] for r in results]
            avg_metrics[key] = sum(values) / len(values) if values else 0.0

        return {
            "individual_results": results,
            "average_metrics": avg_metrics,
            "num_cases": len(results)
        }


# 사용
evaluator = RAGEvaluator()

# 단일 평가
result = evaluator.evaluate(
    question="LangChain이란?",
    answer="LangChain은 LLM 프레임워크입니다.",
    ground_truth="LangChain은 LLM 애플리케이션 개발을 위한 프레임워크입니다.",
    retrieved_docs=["doc1", "doc2", "doc3"],
    relevant_docs=["doc1", "doc4"],
    contexts=["LangChain은 LLM 프레임워크로..."]
)

print("=== 평가 결과 ===")
for metric, value in result.metrics.items():
    print(f"{metric}: {value:.2f}")
