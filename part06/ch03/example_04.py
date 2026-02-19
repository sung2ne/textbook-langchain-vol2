from typing import Dict, List
from datetime import datetime
import json


class EvaluationReporter:
    """평가 리포트 생성기"""

    def generate_text_report(self, run: EvaluationRun) -> str:
        """텍스트 리포트 생성"""
        lines = [
            "=" * 60,
            "RAG 평가 리포트",
            "=" * 60,
            f"실행 ID: {run.run_id}",
            f"시간: {run.timestamp}",
            f"테스트 케이스: {run.num_cases}개",
            f"소요 시간: {run.duration_seconds:.2f}초",
            "",
            "--- 검색 지표 ---",
            f"Precision@5: {run.metrics.get('precision@5', 0):.2%}",
            f"Recall@5:    {run.metrics.get('recall@5', 0):.2%}",
            f"MRR:         {run.metrics.get('mrr', 0):.2%}",
            "",
            "--- 생성 지표 ---",
            f"평균 답변 길이: {run.metrics.get('avg_answer_length', 0):.0f}자",
            "",
            "=" * 60
        ]

        return "\n".join(lines)

    def generate_json_report(self, run: EvaluationRun) -> str:
        """JSON 리포트 생성"""
        report = {
            "run_id": run.run_id,
            "timestamp": run.timestamp,
            "summary": {
                "num_cases": run.num_cases,
                "duration_seconds": run.duration_seconds
            },
            "metrics": run.metrics,
            "config": run.config
        }

        return json.dumps(report, indent=2, ensure_ascii=False)

    def generate_markdown_report(self, run: EvaluationRun) -> str:
        """마크다운 리포트 생성"""
        md = f"""# RAG 평가 리포트

**실행 ID**: {run.run_id}
**시간**: {run.timestamp}

## 요약

| 항목 | 값 |
|------|-----|
| 테스트 케이스 | {run.num_cases}개 |
| 소요 시간 | {run.duration_seconds:.2f}초 |

## 검색 품질

| 지표 | 점수 |
|------|------|
| Precision@5 | {run.metrics.get('precision@5', 0):.2%} |
| Recall@5 | {run.metrics.get('recall@5', 0):.2%} |
| MRR | {run.metrics.get('mrr', 0):.2%} |

## 생성 품질

| 지표 | 값 |
|------|-----|
| 평균 답변 길이 | {run.metrics.get('avg_answer_length', 0):.0f}자 |

"""
        return md

    def compare_runs(self, runs: List[EvaluationRun]) -> str:
        """여러 실행 비교"""
        if not runs:
            return "비교할 실행이 없습니다."

        lines = [
            "=== 실행 비교 ===",
            "",
            f"{'실행 ID':<25} {'Precision':<12} {'Recall':<12} {'MRR':<12}"
        ]
        lines.append("-" * 60)

        for run in runs:
            p = run.metrics.get('precision@5', 0)
            r = run.metrics.get('recall@5', 0)
            mrr = run.metrics.get('mrr', 0)
            lines.append(f"{run.run_id:<25} {p:<12.2%} {r:<12.2%} {mrr:<12.2%}")

        # 최고 성능 표시
        best_p = max(runs, key=lambda x: x.metrics.get('precision@5', 0))
        lines.append("")
        lines.append(f"최고 Precision: {best_p.run_id}")

        return "\n".join(lines)


# 사용
reporter = EvaluationReporter()

# 리포트 생성
print(reporter.generate_text_report(run))
