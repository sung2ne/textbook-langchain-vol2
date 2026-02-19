from typing import Dict, List, Callable
from dataclasses import dataclass


@dataclass
class ImprovementAction:
    """개선 조치"""
    area: str
    action: str
    priority: int
    expected_impact: str


class RAGImprovementSystem:
    """RAG 종합 개선 시스템"""

    def __init__(self, rag_system):
        self.rag_system = rag_system
        self.diagnostics = RAGDiagnostics()
        self.history: List[Dict] = []

    def analyze_and_recommend(self, metrics: Dict[str, float]) -> List[ImprovementAction]:
        """분석 및 개선 권장"""
        issues = self.diagnostics.diagnose(metrics)
        actions = []

        for issue in issues:
            action = self._issue_to_action(issue)
            if action:
                actions.append(action)

        # 우선순위 정렬
        actions.sort(key=lambda x: x.priority)

        return actions

    def _issue_to_action(self, issue: DiagnosticResult) -> ImprovementAction:
        """이슈를 액션으로 변환"""
        priority_map = {"high": 1, "medium": 2, "low": 3}

        action_map = {
            "검색": {
                "Precision": ImprovementAction(
                    area="검색",
                    action="임베딩 모델 변경 또는 청킹 크기 조정",
                    priority=priority_map[issue.severity],
                    expected_impact="Precision 10-20% 향상"
                ),
                "Recall": ImprovementAction(
                    area="검색",
                    action="검색 결과 수(k) 증가 또는 하이브리드 검색",
                    priority=priority_map[issue.severity],
                    expected_impact="Recall 15-25% 향상"
                ),
                "MRR": ImprovementAction(
                    area="검색",
                    action="리랭킹 도입",
                    priority=priority_map[issue.severity],
                    expected_impact="MRR 5-15% 향상"
                )
            },
            "생성": {
                "충실도": ImprovementAction(
                    area="생성",
                    action="프롬프트 강화 (strict 모드)",
                    priority=priority_map[issue.severity],
                    expected_impact="환각 30-50% 감소"
                )
            },
            "성능": {
                "지연": ImprovementAction(
                    area="성능",
                    action="캐싱 및 배치 처리 도입",
                    priority=priority_map[issue.severity],
                    expected_impact="지연 시간 40-60% 감소"
                )
            }
        }

        for keyword, action in action_map.get(issue.area, {}).items():
            if keyword in issue.issue:
                return action

        return ImprovementAction(
            area=issue.area,
            action=issue.recommendation,
            priority=priority_map.get(issue.severity, 2),
            expected_impact="측정 필요"
        )

    def apply_improvement(self, action: ImprovementAction,
                         implementation: Callable) -> Dict:
        """개선 적용"""
        print(f"🔧 개선 적용: {action.action}")

        # 적용 전 메트릭
        before_metrics = self._get_current_metrics()

        # 개선 적용
        implementation()

        # 적용 후 메트릭
        after_metrics = self._get_current_metrics()

        # 결과 기록
        result = {
            "action": action,
            "before": before_metrics,
            "after": after_metrics,
            "improvement": {
                k: after_metrics.get(k, 0) - before_metrics.get(k, 0)
                for k in before_metrics
            }
        }

        self.history.append(result)

        return result

    def _get_current_metrics(self) -> Dict[str, float]:
        """현재 메트릭 조회 (구현 필요)"""
        # 실제로는 평가 실행
        return {
            "precision@5": 0.7,
            "recall@5": 0.6,
            "mrr": 0.75
        }

    def generate_improvement_plan(self, metrics: Dict[str, float]) -> str:
        """개선 계획 생성"""
        actions = self.analyze_and_recommend(metrics)

        plan = ["=== RAG 개선 계획 ===", ""]

        for i, action in enumerate(actions, 1):
            plan.append(f"{i}. [{action.area}] {action.action}")
            plan.append(f"   예상 효과: {action.expected_impact}")
            plan.append("")

        if not actions:
            plan.append("현재 시스템은 양호한 상태입니다.")

        return "\n".join(plan)


# 사용
improvement_system = RAGImprovementSystem(mock_rag_system)

current_metrics = {
    "precision@5": 0.55,
    "recall@5": 0.45,
    "mrr": 0.60,
    "faithfulness": 0.65,
    "latency_ms": 2000
}

# 개선 계획 생성
plan = improvement_system.generate_improvement_plan(current_metrics)
print(plan)

# 개선 권장 사항
actions = improvement_system.analyze_and_recommend(current_metrics)
print(f"\n총 {len(actions)}개 개선 항목 발견")
