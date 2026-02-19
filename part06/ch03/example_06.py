from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path


class RegressionTester:
    """회귀 테스트"""

    def __init__(self, baseline_path: str = "baseline_metrics.json"):
        self.baseline_path = Path(baseline_path)

    def save_baseline(self, metrics: Dict[str, float]):
        """베이스라인 저장"""
        data = {
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }

        with open(self.baseline_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"베이스라인 저장: {self.baseline_path}")

    def load_baseline(self) -> Optional[Dict]:
        """베이스라인 로드"""
        if not self.baseline_path.exists():
            return None

        with open(self.baseline_path, "r") as f:
            return json.load(f)

    def compare_to_baseline(self, current_metrics: Dict[str, float],
                           tolerance: float = 0.05) -> Dict:
        """베이스라인과 비교"""
        baseline = self.load_baseline()

        if not baseline:
            return {
                "status": "no_baseline",
                "message": "베이스라인 없음. 현재 결과를 베이스라인으로 저장하세요."
            }

        baseline_metrics = baseline["metrics"]
        regressions = []
        improvements = []

        for metric, current in current_metrics.items():
            if metric not in baseline_metrics:
                continue

            base_value = baseline_metrics[metric]
            diff = current - base_value
            diff_pct = diff / base_value if base_value > 0 else 0

            if diff_pct < -tolerance:
                regressions.append({
                    "metric": metric,
                    "baseline": base_value,
                    "current": current,
                    "diff": diff,
                    "diff_pct": diff_pct
                })
            elif diff_pct > tolerance:
                improvements.append({
                    "metric": metric,
                    "baseline": base_value,
                    "current": current,
                    "diff": diff,
                    "diff_pct": diff_pct
                })

        return {
            "status": "regression" if regressions else "ok",
            "regressions": regressions,
            "improvements": improvements,
            "baseline_timestamp": baseline["timestamp"]
        }

    def print_comparison(self, comparison: Dict):
        """비교 결과 출력"""
        if comparison["status"] == "no_baseline":
            print(comparison["message"])
            return

        print(f"베이스라인: {comparison['baseline_timestamp']}")
        print()

        if comparison["regressions"]:
            print("⚠️ 회귀 발견:")
            for reg in comparison["regressions"]:
                print(f"  {reg['metric']}: {reg['baseline']:.2%} → {reg['current']:.2%} "
                      f"({reg['diff_pct']:+.1%})")

        if comparison["improvements"]:
            print("\n✅ 개선:")
            for imp in comparison["improvements"]:
                print(f"  {imp['metric']}: {imp['baseline']:.2%} → {imp['current']:.2%} "
                      f"({imp['diff_pct']:+.1%})")

        if not comparison["regressions"] and not comparison["improvements"]:
            print("변화 없음 (허용 범위 내)")


# 사용
regression_tester = RegressionTester()

# 베이스라인 저장 (최초 또는 릴리스 시)
baseline_metrics = {"precision@5": 0.75, "recall@5": 0.65, "mrr": 0.80}
# regression_tester.save_baseline(baseline_metrics)

# 현재 결과와 비교
current_metrics = {"precision@5": 0.78, "recall@5": 0.58, "mrr": 0.81}
comparison = regression_tester.compare_to_baseline(current_metrics, tolerance=0.05)
regression_tester.print_comparison(comparison)
