# app/services/cache_service.py
from typing import Optional, Any
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta


class CacheService:
    """캐싱 서비스"""

    def __init__(self, cache_dir: str = "./data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=24)

    def _get_key(self, prefix: str, data: str) -> str:
        """캐시 키 생성"""
        hash_val = hashlib.md5(data.encode()).hexdigest()
        return f"{prefix}_{hash_val}"

    def get(self, key: str) -> Optional[Any]:
        """캐시 조회"""
        cache_file = self.cache_dir / f"{key}.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "r") as f:
                cached = json.load(f)

            # TTL 확인
            cached_time = datetime.fromisoformat(cached["timestamp"])
            if datetime.now() - cached_time > self.ttl:
                cache_file.unlink()
                return None

            return cached["data"]

        except Exception:
            return None

    def set(self, key: str, data: Any):
        """캐시 저장"""
        cache_file = self.cache_dir / f"{key}.json"

        cached = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }

        with open(cache_file, "w") as f:
            json.dump(cached, f)

    def delete(self, key: str):
        """캐시 삭제"""
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            cache_file.unlink()

    def clear(self):
        """전체 캐시 삭제"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()


class QueryCache:
    """질의 캐시"""

    def __init__(self):
        self.cache = CacheService()

    def get_cached_answer(self, question: str,
                         k: int) -> Optional[dict]:
        """캐시된 답변 조회"""
        key = self.cache._get_key("query", f"{question}_{k}")
        return self.cache.get(key)

    def cache_answer(self, question: str, k: int, response: dict):
        """답변 캐시"""
        key = self.cache._get_key("query", f"{question}_{k}")
        self.cache.set(key, response)
