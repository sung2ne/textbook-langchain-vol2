from dataclasses import dataclass
from enum import Enum
from typing import List


class QueryType(Enum):
    FACTUAL = "factual"      # 사실 확인 질문
    COMPARISON = "comparison" # 비교 질문
    HOWTO = "howto"          # 방법 질문
    CONCEPTUAL = "conceptual" # 개념 질문
    GENERAL = "general"      # 일반


@dataclass
class QueryAnalysis:
    query_type: QueryType
    keywords: List[str]
    is_technical: bool
    complexity: str  # "simple", "medium", "complex"
    suggested_k: int


class QueryAnalyzer:
    """쿼리 분석기"""

    def analyze(self, query: str) -> QueryAnalysis:
        """쿼리 분석"""
        query_lower = query.lower()

        # 쿼리 타입 결정
        if any(word in query_lower for word in ["뭐", "무엇", "정의", "의미"]):
            query_type = QueryType.FACTUAL
        elif any(word in query_lower for word in ["비교", "차이", "vs", "다른"]):
            query_type = QueryType.COMPARISON
        elif any(word in query_lower for word in ["어떻게", "방법", "하려면"]):
            query_type = QueryType.HOWTO
        elif any(word in query_lower for word in ["왜", "원리", "이유"]):
            query_type = QueryType.CONCEPTUAL
        else:
            query_type = QueryType.GENERAL

        # 키워드 추출 (간단한 방식)
        keywords = [word for word in query.split() if len(word) > 1]

        # 기술 문서 여부
        tech_terms = ["api", "함수", "클래스", "코드", "에러", "설치", "구현"]
        is_technical = any(term in query_lower for term in tech_terms)

        # 복잡도
        if len(query) < 20:
            complexity = "simple"
        elif len(query) < 50:
            complexity = "medium"
        else:
            complexity = "complex"

        # 권장 k 값
        suggested_k = 3 if complexity == "simple" else 5 if complexity == "medium" else 7

        return QueryAnalysis(
            query_type=query_type,
            keywords=keywords,
            is_technical=is_technical,
            complexity=complexity,
            suggested_k=suggested_k
        )


# 사용
analyzer = QueryAnalyzer()

queries = [
    "LangChain이 뭐야?",
    "LangChain과 LlamaIndex 차이점",
    "RAG 시스템 어떻게 구축해?",
]

for q in queries:
    analysis = analyzer.analyze(q)
    print(f"쿼리: {q}")
    print(f"  타입: {analysis.query_type.value}")
    print(f"  기술: {analysis.is_technical}")
    print(f"  복잡도: {analysis.complexity}")
    print()
