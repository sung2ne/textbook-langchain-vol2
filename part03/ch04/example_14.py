from functools import lru_cache


class CachedRAG(RAGSystem):
    @lru_cache(maxsize=100)
    def _cached_search(self, query):
        return tuple(self.search(query, k=3))

    def ask(self, question):
        # 캐시된 검색 사용
        docs = self._cached_search(question)
        # ... 답변 생성
