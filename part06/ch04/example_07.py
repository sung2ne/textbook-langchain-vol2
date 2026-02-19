from functools import lru_cache
from typing import Dict, Optional
import hashlib
import time


class PerformanceOptimizer:
    """성능 최적화"""

    def __init__(self):
        self.query_cache: Dict[str, Dict] = {}
        self.cache_ttl = 3600  # 1시간

    def _get_cache_key(self, query: str) -> str:
        """캐시 키 생성"""
        return hashlib.md5(query.encode()).hexdigest()

    def cached_search(self, query: str, search_func) -> Dict:
        """캐시된 검색"""
        key = self._get_cache_key(query)

        # 캐시 확인
        if key in self.query_cache:
            cached = self.query_cache[key]
            if time.time() - cached["timestamp"] < self.cache_ttl:
                cached["cache_hit"] = True
                return cached

        # 새로 검색
        result = search_func(query)
        result["timestamp"] = time.time()
        result["cache_hit"] = False

        self.query_cache[key] = result
        return result

    def clear_cache(self):
        """캐시 초기화"""
        self.query_cache.clear()

    def get_cache_stats(self) -> Dict:
        """캐시 통계"""
        return {
            "size": len(self.query_cache),
            "keys": list(self.query_cache.keys())[:10]
        }


class BatchOptimizer:
    """배치 최적화"""

    def __init__(self, embeddings):
        self.embeddings = embeddings

    def batch_embed(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """배치 임베딩"""
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            embeddings = self.embeddings.embed_documents(batch)
            all_embeddings.extend(embeddings)

        return all_embeddings


# 사용
optimizer = PerformanceOptimizer()

def mock_search(query):
    time.sleep(0.1)  # 시뮬레이션
    return {"results": [f"Result for {query}"]}

# 첫 번째 호출 (캐시 미스)
result1 = optimizer.cached_search("test query", mock_search)
print(f"Cache hit: {result1['cache_hit']}")

# 두 번째 호출 (캐시 히트)
result2 = optimizer.cached_search("test query", mock_search)
print(f"Cache hit: {result2['cache_hit']}")
