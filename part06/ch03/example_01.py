from typing import List, Dict, Callable
from dataclasses import dataclass
import json
import time
from datetime import datetime


@dataclass
class EvaluationRun:
    """평가 실행 결과"""
    run_id: str
    timestamp: str
    num_cases: int
    metrics: Dict[str, float]
    duration_seconds: float
    config: Dict


class AutomatedEvaluator:
    """자동화된 평가기"""

    def __init__(self, rag_system: Callable):
        self.rag_system = rag_system
        self.runs: List[EvaluationRun] = []

    def run_evaluation(self, test_cases: List[Dict],
                      config: Dict = None) -> EvaluationRun:
        """평가 실행"""
        run_id = f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = time.time()

        results = []

        for case in test_cases:
            # RAG 시스템 호출
            question = case["question"]
            response = self.rag_system(question)

            result = {
                "question": question,
                "expected": case.get("ground_truth", ""),
                "actual": response.get("answer", ""),
                "contexts": response.get("contexts", []),
                "retrieved_docs": response.get("retrieved_docs", []),
                "relevant_docs": case.get("relevant_doc_ids", [])
            }
            results.append(result)

        # 지표 계산
        metrics = self._calculate_metrics(results)

        duration = time.time() - start_time

        run = EvaluationRun(
            run_id=run_id,
            timestamp=datetime.now().isoformat(),
            num_cases=len(test_cases),
            metrics=metrics,
            duration_seconds=duration,
            config=config or {}
        )

        self.runs.append(run)
        return run

    def _calculate_metrics(self, results: List[Dict]) -> Dict[str, float]:
        """지표 계산"""
        metrics = {
            "precision@5": 0.0,
            "recall@5": 0.0,
            "mrr": 0.0,
            "avg_answer_length": 0.0
        }

        if not results:
            return metrics

        total_precision = 0.0
        total_recall = 0.0
        total_mrr = 0.0
        total_answer_length = 0

        for result in results:
            retrieved = result["retrieved_docs"][:5]
            relevant = set(result["relevant_docs"])

            # Precision@5
            if retrieved:
                hits = len(set(retrieved) & relevant)
                total_precision += hits / len(retrieved)

            # Recall@5
            if relevant:
                hits = len(set(retrieved) & relevant)
                total_recall += hits / len(relevant)

            # MRR
            for i, doc in enumerate(retrieved):
                if doc in relevant:
                    total_mrr += 1.0 / (i + 1)
                    break

            # 답변 길이
            total_answer_length += len(result["actual"])

        n = len(results)
        metrics["precision@5"] = total_precision / n
        metrics["recall@5"] = total_recall / n
        metrics["mrr"] = total_mrr / n
        metrics["avg_answer_length"] = total_answer_length / n

        return metrics


# 사용 예시 (Mock RAG 시스템)
def mock_rag_system(question: str) -> Dict:
    """테스트용 Mock RAG"""
    return {
        "answer": f"Mock 답변: {question}",
        "contexts": ["context1", "context2"],
        "retrieved_docs": ["doc1", "doc2", "doc3"]
    }


evaluator = AutomatedEvaluator(mock_rag_system)

test_cases = [
    {"question": "Q1?", "ground_truth": "A1", "relevant_doc_ids": ["doc1", "doc2"]},
    {"question": "Q2?", "ground_truth": "A2", "relevant_doc_ids": ["doc3"]},
]

run = evaluator.run_evaluation(test_cases)
print(f"Run ID: {run.run_id}")
print(f"Precision@5: {run.metrics['precision@5']:.2f}")
print(f"Duration: {run.duration_seconds:.2f}s")
