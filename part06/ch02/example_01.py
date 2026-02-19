from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json
from datetime import datetime


@dataclass
class TestCase:
    """테스트 케이스"""
    question: str
    ground_truth: str
    relevant_doc_ids: List[str]
    difficulty: str = "medium"  # easy, medium, hard
    category: str = "general"
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """딕셔너리 변환"""
        return {
            "question": self.question,
            "ground_truth": self.ground_truth,
            "relevant_doc_ids": self.relevant_doc_ids,
            "difficulty": self.difficulty,
            "category": self.category,
            "metadata": self.metadata
        }


class TestSetBuilder:
    """테스트셋 빌더"""

    def __init__(self, name: str):
        self.name = name
        self.test_cases: List[TestCase] = []
        self.created_at = datetime.now().isoformat()

    def add_case(self, question: str, ground_truth: str,
                relevant_doc_ids: List[str], **kwargs) -> "TestSetBuilder":
        """테스트 케이스 추가"""
        case = TestCase(
            question=question,
            ground_truth=ground_truth,
            relevant_doc_ids=relevant_doc_ids,
            **kwargs
        )
        self.test_cases.append(case)
        return self

    def save(self, path: str):
        """저장"""
        data = {
            "name": self.name,
            "created_at": self.created_at,
            "num_cases": len(self.test_cases),
            "test_cases": [tc.to_dict() for tc in self.test_cases]
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str) -> "TestSetBuilder":
        """로드"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        builder = cls(data["name"])
        builder.created_at = data["created_at"]

        for case_data in data["test_cases"]:
            builder.add_case(**case_data)

        return builder


# 사용
builder = TestSetBuilder("LangChain 기초 테스트셋")

builder.add_case(
    question="LangChain이란 무엇인가요?",
    ground_truth="LangChain은 LLM 애플리케이션 개발을 위한 프레임워크입니다.",
    relevant_doc_ids=["doc_001", "doc_002"],
    difficulty="easy",
    category="introduction"
)

builder.add_case(
    question="RAG에서 검색과 생성의 역할은?",
    ground_truth="검색은 관련 문서를 찾고, 생성은 문서를 바탕으로 답변을 만듭니다.",
    relevant_doc_ids=["doc_010", "doc_011", "doc_012"],
    difficulty="medium",
    category="rag"
)

builder.add_case(
    question="벡터 데이터베이스 선택 기준은?",
    ground_truth="성능, 확장성, 비용, 기능을 고려해야 합니다.",
    relevant_doc_ids=["doc_020", "doc_021"],
    difficulty="hard",
    category="vector_db"
)

# 저장
builder.save("test_set.json")
print(f"테스트 케이스 {len(builder.test_cases)}개 저장")
