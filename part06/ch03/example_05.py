from typing import Dict
import sys


class ThresholdChecker:
    """임계값 검사기"""

    def __init__(self, thresholds: Dict[str, float]):
        self.thresholds = thresholds

    def check(self, metrics: Dict[str, float]) -> Dict:
        """임계값 검사"""
        results = {
            "passed": True,
            "checks": []
        }

        for metric, threshold in self.thresholds.items():
            actual = metrics.get(metric, 0)
            passed = actual >= threshold

            results["checks"].append({
                "metric": metric,
                "threshold": threshold,
                "actual": actual,
                "passed": passed
            })

            if not passed:
                results["passed"] = False

        return results

    def print_results(self, results: Dict):
        """결과 출력"""
        print("=== 임계값 검사 결과 ===")

        for check in results["checks"]:
            status = "✅" if check["passed"] else "❌"
            print(f"{status} {check['metric']}: {check['actual']:.2%} "
                  f"(임계값: {check['threshold']:.2%})")

        print()
        if results["passed"]:
            print("🎉 모든 검사 통과!")
        else:
            print("⚠️ 일부 검사 실패")

    def exit_on_failure(self, results: Dict):
        """실패 시 종료 (CI용)"""
        if not results["passed"]:
            self.print_results(results)
            sys.exit(1)


# 사용
thresholds = {
    "precision@5": 0.7,
    "recall@5": 0.6,
    "mrr": 0.75
}

checker = ThresholdChecker(thresholds)

# 실제 메트릭
metrics = {
    "precision@5": 0.75,
    "recall@5": 0.55,  # 임계값 미달
    "mrr": 0.80
}

results = checker.check(metrics)
checker.print_results(results)

# CI에서는
# checker.exit_on_failure(results)
