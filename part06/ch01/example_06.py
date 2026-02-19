import json
from typing import Dict, List


def print_evaluation_report(results: Dict):
    """평가 리포트 출력"""
    print("=" * 50)
    print("RAG 평가 리포트")
    print("=" * 50)

    avg = results["average_metrics"]

    # 검색 지표
    print("\n📊 검색 품질")
    print(f"  Precision@5: {avg.get('precision@5', 0):.2%}")
    print(f"  Recall@5:    {avg.get('recall@5', 0):.2%}")
    print(f"  MRR:         {avg.get('mrr', 0):.2%}")

    # 생성 지표
    print("\n📝 생성 품질")
    print(f"  충실도:      {avg.get('faithfulness', 0):.2%}")
    print(f"  관련성:      {avg.get('relevance', 0):.2%}")
    print(f"  정확성:      {avg.get('correctness', 0):.2%}")

    # 종합 점수
    all_scores = list(avg.values())
    overall = sum(all_scores) / len(all_scores) if all_scores else 0

    print("\n" + "=" * 50)
    print(f"종합 점수: {overall:.2%}")
    print("=" * 50)

    # 등급
    if overall >= 0.9:
        grade = "A (우수)"
    elif overall >= 0.8:
        grade = "B (양호)"
    elif overall >= 0.7:
        grade = "C (보통)"
    elif overall >= 0.6:
        grade = "D (개선 필요)"
    else:
        grade = "F (미흡)"

    print(f"등급: {grade}")


# 예시 결과
sample_results = {
    "average_metrics": {
        "precision@5": 0.75,
        "recall@5": 0.60,
        "mrr": 0.80,
        "faithfulness": 0.85,
        "relevance": 0.90,
        "correctness": 0.80
    },
    "num_cases": 100
}

print_evaluation_report(sample_results)
