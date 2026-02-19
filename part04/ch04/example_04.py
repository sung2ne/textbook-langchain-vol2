from functools import lru_cache
import hashlib
import json


class CachedSearchPipeline:
    """캐싱이 적용된 검색 파이프라인"""

    def __init__(self, base_pipeline: SearchPipeline, cache_size: int = 100):
        self.pipeline = base_pipeline
        self.cache = {}
        self.cache_size = cache_size

    def _hash_query(self, query: str) -> str:
        """쿼리 해시 생성"""
        return hashlib.md5(query.encode()).hexdigest()

    def search(self, query: str, use_cache: bool = True) -> SearchResult:
        """캐시 적용 검색"""
        query_hash = self._hash_query(query)

        # 캐시 확인
        if use_cache and query_hash in self.cache:
            print("캐시 히트!")
            return self.cache[query_hash]

        # 검색 실행
        result = self.pipeline.search(query)

        # 캐시 저장
        if len(self.cache) >= self.cache_size:
            # 오래된 항목 제거 (FIFO)
            oldest = next(iter(self.cache))
            del self.cache[oldest]

        self.cache[query_hash] = result

        return result

    def clear_cache(self):
        """캐시 초기화"""
        self.cache.clear()
