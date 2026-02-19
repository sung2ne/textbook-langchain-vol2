from typing import Dict, List
from dataclasses import dataclass


@dataclass
class DiagnosticResult:
    """진단 결과"""
    area: str
    severity: str  # low, medium, high
    issue: str
    recommendation: str


class RAGDiagnostics:
    """RAG 진단 도구"""

    def __init__(self, thresholds: Dict[str, float] = None):
        self.thresholds = thresholds or {
            "precision@5": 0.7,
            "recall@5": 0.6,
            "mrr": 0.75,
            "faithfulness": 0.8,
            "latency_ms": 1000
        }

    def diagnose(self, metrics: Dict[str, float]) -> List[DiagnosticResult]:
        """진단 실행"""
        issues = []

        # Precision 진단
        precision = metrics.get("precision@5", 0)
        if precision < self.thresholds["precision@5"]:
            severity = "high" if precision < 0.5 else "medium"
            issues.append(DiagnosticResult(
                area="검색",
                severity=severity,
                issue=f"Precision@5이 낮음 ({precision:.2%})",
                recommendation="임베딩 모델 변경, 청킹 전략 개선"
            ))

        # Recall 진단
        recall = metrics.get("recall@5", 0)
        if recall < self.thresholds["recall@5"]:
            severity = "high" if recall < 0.4 else "medium"
            issues.append(DiagnosticResult(
                area="검색",
                severity=severity,
                issue=f"Recall@5이 낮음 ({recall:.2%})",
                recommendation="k 값 증가, 하이브리드 검색 도입"
            ))

        # MRR 진단
        mrr = metrics.get("mrr", 0)
        if mrr < self.thresholds["mrr"]:
            issues.append(DiagnosticResult(
                area="검색",
                severity="medium",
                issue=f"MRR이 낮음 ({mrr:.2%})",
                recommendation="리랭킹 도입, 쿼리 변환 적용"
            ))

        # Faithfulness 진단
        faithfulness = metrics.get("faithfulness", 0)
        if faithfulness < self.thresholds["faithfulness"]:
            severity = "high" if faithfulness < 0.6 else "medium"
            issues.append(DiagnosticResult(
                area="생성",
                severity=severity,
                issue=f"충실도가 낮음 ({faithfulness:.2%})",
                recommendation="프롬프트 개선, 컨텍스트 제한"
            ))

        # 지연 시간 진단
        latency = metrics.get("latency_ms", 0)
        if latency > self.thresholds["latency_ms"]:
            severity = "high" if latency > 3000 else "medium"
            issues.append(DiagnosticResult(
                area="성능",
                severity=severity,
                issue=f"지연 시간이 높음 ({latency:.0f}ms)",
                recommendation="인덱스 최적화, 캐싱 도입"
            ))

        return issues

    def print_report(self, issues: List[DiagnosticResult]):
        """진단 리포트 출력"""
        if not issues:
            print("✅ 발견된 문제가 없습니다!")
            return

        print("=== RAG 진단 리포트 ===\n")

        severity_order = {"high": 0, "medium": 1, "low": 2}
        sorted_issues = sorted(issues, key=lambda x: severity_order[x.severity])

        for issue in sorted_issues:
            emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}[issue.severity]
            print(f"{emoji} [{issue.area}] {issue.issue}")
            print(f"   → {issue.recommendation}")
            print()


# 사용
diagnostics = RAGDiagnostics()

metrics = {
    "precision@5": 0.55,
    "recall@5": 0.45,
    "mrr": 0.65,
    "faithfulness": 0.70,
    "latency_ms": 1500
}

issues = diagnostics.diagnose(metrics)
diagnostics.print_report(issues)
