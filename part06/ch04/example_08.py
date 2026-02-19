from typing import Dict, List, Callable
import random
from dataclasses import dataclass


@dataclass
class ABTestResult:
    """A/B 테스트 결과"""
    variant_a_metrics: Dict[str, float]
    variant_b_metrics: Dict[str, float]
    winner: str
    confidence: float


class ABTester:
    """A/B 테스트"""

    def __init__(self):
        self.results: Dict[str, List] = {"A": [], "B": []}

    def run_test(self, test_cases: List[Dict],
                variant_a: Callable, variant_b: Callable,
                metric_func: Callable) -> ABTestResult:
        """A/B 테스트 실행"""

        for case in test_cases:
            # 랜덤 배정
            if random.random() < 0.5:
                result = variant_a(case)
                score = metric_func(result, case)
                self.results["A"].append(score)
            else:
                result = variant_b(case)
                score = metric_func(result, case)
                self.results["B"].append(score)

        # 결과 분석
        metrics_a = self._calculate_metrics(self.results["A"])
        metrics_b = self._calculate_metrics(self.results["B"])

        winner, confidence = self._determine_winner(
            self.results["A"], self.results["B"]
        )

        return ABTestResult(
            variant_a_metrics=metrics_a,
            variant_b_metrics=metrics_b,
            winner=winner,
            confidence=confidence
        )

    def _calculate_metrics(self, scores: List[float]) -> Dict[str, float]:
        """메트릭 계산"""
        if not scores:
            return {"mean": 0, "count": 0}

        return {
            "mean": sum(scores) / len(scores),
            "count": len(scores),
            "min": min(scores),
            "max": max(scores)
        }

    def _determine_winner(self, scores_a: List[float],
                         scores_b: List[float]) -> tuple:
        """승자 결정"""
        if not scores_a or not scores_b:
            return "inconclusive", 0.0

        mean_a = sum(scores_a) / len(scores_a)
        mean_b = sum(scores_b) / len(scores_b)

        diff = abs(mean_a - mean_b)
        avg = (mean_a + mean_b) / 2

        # 단순화된 신뢰도 (실제로는 통계 검정 필요)
        confidence = min(diff / max(avg, 0.01), 1.0)

        if mean_a > mean_b:
            winner = "A"
        elif mean_b > mean_a:
            winner = "B"
        else:
            winner = "tie"

        return winner, confidence


# 사용
ab_tester = ABTester()

# 두 가지 변형
def variant_a(case):
    return {"answer": "A: " + case.get("question", "")}

def variant_b(case):
    return {"answer": "B: " + case.get("question", "")}

def score_func(result, case):
    # 단순화된 점수 (실제로는 품질 평가)
    return random.uniform(0.6, 0.9)

test_cases = [{"question": f"Q{i}"} for i in range(100)]

result = ab_tester.run_test(test_cases, variant_a, variant_b, score_func)

print(f"Variant A: {result.variant_a_metrics['mean']:.2f}")
print(f"Variant B: {result.variant_b_metrics['mean']:.2f}")
print(f"Winner: {result.winner} (confidence: {result.confidence:.2%})")
