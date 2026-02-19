import time
from dataclasses import dataclass, field
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SearchMetrics:
    query: str
    total_time: float
    analysis_time: float
    retrieval_time: float
    rerank_time: float
    initial_count: int
    final_count: int


class MonitoredSearchPipeline:
    """모니터링이 적용된 검색 파이프라인"""

    def __init__(self, base_pipeline: SearchPipeline):
        self.pipeline = base_pipeline
        self.metrics_history: List[SearchMetrics] = []

    def search(self, query: str) -> Tuple[SearchResult, SearchMetrics]:
        """검색 및 메트릭 수집"""
        total_start = time.time()

        # 분석 시간
        analysis_start = time.time()
        analysis = self.pipeline.analyzer.analyze(query)
        analysis_time = time.time() - analysis_start

        strategy = self.pipeline.selector.select(analysis)

        # 검색 시간
        retrieval_start = time.time()
        queries = [query]
        if strategy.use_query_expansion:
            queries.extend(self.pipeline._expand_query(query))

        initial_results = self.pipeline._initial_search(queries, strategy)
        retrieval_time = time.time() - retrieval_start

        # 리랭킹 시간
        rerank_start = time.time()
        if strategy.use_reranking and initial_results:
            final_results = self.pipeline._rerank(query, initial_results, strategy.final_k)
        else:
            final_results = [(doc, 1.0) for doc in initial_results[:strategy.final_k]]
        rerank_time = time.time() - rerank_start

        total_time = time.time() - total_start

        # 메트릭 생성
        metrics = SearchMetrics(
            query=query,
            total_time=total_time,
            analysis_time=analysis_time,
            retrieval_time=retrieval_time,
            rerank_time=rerank_time,
            initial_count=len(initial_results),
            final_count=len(final_results)
        )

        self.metrics_history.append(metrics)

        # 로깅
        logger.info(f"검색 완료: {query[:30]}... ({total_time:.3f}초)")

        result = SearchResult(
            documents=final_results,
            query_analysis=analysis,
            strategy=strategy
        )

        return result, metrics

    def get_stats(self) -> Dict:
        """통계 반환"""
        if not self.metrics_history:
            return {}

        total_times = [m.total_time for m in self.metrics_history]

        return {
            "total_queries": len(self.metrics_history),
            "avg_time": sum(total_times) / len(total_times),
            "max_time": max(total_times),
            "min_time": min(total_times),
        }

    def print_report(self):
        """성능 리포트 출력"""
        stats = self.get_stats()
        print("\n=== 검색 성능 리포트 ===")
        print(f"총 검색 수: {stats.get('total_queries', 0)}")
        print(f"평균 시간: {stats.get('avg_time', 0):.3f}초")
        print(f"최대 시간: {stats.get('max_time', 0):.3f}초")
        print(f"최소 시간: {stats.get('min_time', 0):.3f}초")


# 사용
monitored = MonitoredSearchPipeline(pipeline)

for q in queries:
    result, metrics = monitored.search(q)
    print(f"  분석: {metrics.analysis_time:.3f}초")
    print(f"  검색: {metrics.retrieval_time:.3f}초")
    print(f"  리랭킹: {metrics.rerank_time:.3f}초")

monitored.print_report()
