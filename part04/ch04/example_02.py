from dataclasses import dataclass


@dataclass
class SearchStrategy:
    use_query_expansion: bool
    use_hybrid: bool
    use_reranking: bool
    bm25_weight: float
    initial_k: int
    final_k: int


class StrategySelector:
    """검색 전략 선택기"""

    def select(self, analysis: QueryAnalysis) -> SearchStrategy:
        """분석 결과에 따른 전략 선택"""

        # 기본값
        strategy = SearchStrategy(
            use_query_expansion=False,
            use_hybrid=True,
            use_reranking=True,
            bm25_weight=0.5,
            initial_k=20,
            final_k=analysis.suggested_k
        )

        # 타입별 조정
        if analysis.query_type == QueryType.COMPARISON:
            strategy.use_query_expansion = True
            strategy.initial_k = 30

        elif analysis.query_type == QueryType.HOWTO:
            strategy.bm25_weight = 0.4
            strategy.initial_k = 25

        elif analysis.query_type == QueryType.FACTUAL:
            strategy.bm25_weight = 0.6

        # 기술 문서 조정
        if analysis.is_technical:
            strategy.bm25_weight = 0.6

        # 복잡도 조정
        if analysis.complexity == "complex":
            strategy.use_query_expansion = True
            strategy.initial_k = 30

        return strategy


# 사용
selector = StrategySelector()

for q in queries:
    analysis = analyzer.analyze(q)
    strategy = selector.select(analysis)
    print(f"쿼리: {q}")
    print(f"  확장: {strategy.use_query_expansion}")
    print(f"  하이브리드: {strategy.use_hybrid}")
    print(f"  BM25 가중치: {strategy.bm25_weight}")
    print()
