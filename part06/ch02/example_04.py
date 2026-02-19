from typing import List, Dict
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """검증 결과"""
    is_valid: bool
    issues: List[str]
    score: float


class TestSetValidator:
    """테스트셋 검증기"""

    def __init__(self):
        self.min_question_length = 10
        self.min_answer_length = 20
        self.max_question_length = 500
        self.max_answer_length = 1000

    def validate_case(self, case: Dict) -> ValidationResult:
        """단일 케이스 검증"""
        issues = []
        score = 1.0

        question = case.get("question", "")
        answer = case.get("ground_truth", case.get("answer", ""))

        # 질문 검증
        if len(question) < self.min_question_length:
            issues.append(f"질문이 너무 짧음 ({len(question)}자)")
            score -= 0.2

        if len(question) > self.max_question_length:
            issues.append(f"질문이 너무 김 ({len(question)}자)")
            score -= 0.1

        if not question.endswith("?") and "?" not in question:
            issues.append("질문에 물음표 없음")
            score -= 0.1

        # 답변 검증
        if len(answer) < self.min_answer_length:
            issues.append(f"답변이 너무 짧음 ({len(answer)}자)")
            score -= 0.2

        if len(answer) > self.max_answer_length:
            issues.append(f"답변이 너무 김 ({len(answer)}자)")
            score -= 0.1

        # 관련 문서 검증
        relevant_docs = case.get("relevant_doc_ids", [])
        if not relevant_docs:
            issues.append("관련 문서 ID 없음")
            score -= 0.3

        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            score=max(0, score)
        )

    def validate_test_set(self, test_cases: List[Dict]) -> Dict:
        """전체 테스트셋 검증"""
        results = []
        valid_count = 0
        total_score = 0

        for case in test_cases:
            result = self.validate_case(case)
            results.append(result)

            if result.is_valid:
                valid_count += 1
            total_score += result.score

        return {
            "total_cases": len(test_cases),
            "valid_cases": valid_count,
            "invalid_cases": len(test_cases) - valid_count,
            "validity_rate": valid_count / len(test_cases) if test_cases else 0,
            "average_score": total_score / len(test_cases) if test_cases else 0,
            "individual_results": results
        }

    def get_recommendations(self, validation_result: Dict) -> List[str]:
        """개선 권장사항"""
        recommendations = []

        if validation_result["validity_rate"] < 0.8:
            recommendations.append("유효성 비율이 80% 미만입니다. 테스트 케이스 검토가 필요합니다.")

        if validation_result["average_score"] < 0.7:
            recommendations.append("평균 품질 점수가 낮습니다. 질문과 답변의 품질을 높이세요.")

        # 공통 이슈 분석
        all_issues = []
        for result in validation_result["individual_results"]:
            all_issues.extend(result.issues)

        if all_issues:
            from collections import Counter
            common_issues = Counter(all_issues).most_common(3)
            for issue, count in common_issues:
                recommendations.append(f"빈번한 이슈: '{issue}' ({count}건)")

        return recommendations


# 사용
validator = TestSetValidator()

# 테스트 케이스
test_cases = [
    {
        "question": "LangChain이란 무엇인가요?",
        "ground_truth": "LangChain은 LLM 애플리케이션 개발을 위한 오픈소스 프레임워크입니다.",
        "relevant_doc_ids": ["doc_001"]
    },
    {
        "question": "설치",  # 너무 짧음
        "ground_truth": "pip install",  # 너무 짧음
        "relevant_doc_ids": []  # 없음
    },
    {
        "question": "RAG에서 검색의 역할은 무엇인가요?",
        "ground_truth": "RAG에서 검색은 사용자 질문과 관련된 문서를 벡터 데이터베이스에서 찾아 LLM에 제공하는 역할을 합니다.",
        "relevant_doc_ids": ["doc_010", "doc_011"]
    }
]

result = validator.validate_test_set(test_cases)

print(f"총 케이스: {result['total_cases']}")
print(f"유효 케이스: {result['valid_cases']}")
print(f"유효성 비율: {result['validity_rate']:.1%}")
print(f"평균 점수: {result['average_score']:.2f}")

print("\n권장사항:")
for rec in validator.get_recommendations(result):
    print(f"  - {rec}")
