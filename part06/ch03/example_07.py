from typing import Dict, List, Callable
from pathlib import Path
import json


class AutomatedEvaluationSystem:
    """완전한 자동화 평가 시스템"""

    def __init__(self, rag_system: Callable,
                output_dir: str = "./eval_results"):
        self.rag_system = rag_system
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.evaluator = AutomatedEvaluator(rag_system)
        self.batch_evaluator = BatchEvaluator(rag_system)
        self.benchmark = PerformanceBenchmark(rag_system)
        self.reporter = EvaluationReporter()
        self.regression_tester = RegressionTester(
            str(self.output_dir / "baseline.json")
        )

    def run_full_evaluation(self, test_cases: List[Dict],
                           config: Dict = None) -> Dict:
        """전체 평가 실행"""
        print("=" * 60)
        print("자동화 평가 시스템")
        print("=" * 60)

        # 1. 품질 평가
        print("\n📊 품질 평가 중...")
        eval_run = self.evaluator.run_evaluation(test_cases, config)

        # 2. 성능 벤치마크
        print("\n⏱️ 성능 벤치마크 중...")
        questions = [tc["question"] for tc in test_cases[:20]]
        latency = self.benchmark.measure_latency(questions)

        # 3. 회귀 테스트
        print("\n🔍 회귀 테스트 중...")
        comparison = self.regression_tester.compare_to_baseline(
            eval_run.metrics
        )

        # 4. 리포트 생성
        print("\n📝 리포트 생성 중...")
        text_report = self.reporter.generate_text_report(eval_run)
        json_report = self.reporter.generate_json_report(eval_run)
        md_report = self.reporter.generate_markdown_report(eval_run)

        # 5. 저장
        run_dir = self.output_dir / eval_run.run_id
        run_dir.mkdir(exist_ok=True)

        (run_dir / "report.txt").write_text(text_report)
        (run_dir / "report.json").write_text(json_report)
        (run_dir / "report.md").write_text(md_report)
        (run_dir / "latency.json").write_text(
            json.dumps(latency, indent=2)
        )

        print(f"\n💾 결과 저장: {run_dir}")

        # 6. 결과 출력
        print("\n" + text_report)

        print("\n=== 성능 ===")
        print(f"평균 지연: {latency['mean']*1000:.1f}ms")
        print(f"P99 지연: {latency['p99']*1000:.1f}ms")

        print("\n=== 회귀 테스트 ===")
        self.regression_tester.print_comparison(comparison)

        return {
            "evaluation": eval_run,
            "latency": latency,
            "regression": comparison,
            "output_dir": str(run_dir)
        }

    def update_baseline(self, metrics: Dict[str, float]):
        """베이스라인 업데이트"""
        self.regression_tester.save_baseline(metrics)


# 사용
system = AutomatedEvaluationSystem(mock_rag_system)

test_cases = [
    {"question": "Q1?", "ground_truth": "A1", "relevant_doc_ids": ["doc1"]},
    {"question": "Q2?", "ground_truth": "A2", "relevant_doc_ids": ["doc2"]},
    {"question": "Q3?", "ground_truth": "A3", "relevant_doc_ids": ["doc1", "doc3"]},
]

result = system.run_full_evaluation(test_cases, {"version": "1.0"})
