# app/utils/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from functools import wraps
import time


# 카운터
REQUEST_COUNT = Counter(
    "rag_requests_total",
    "Total requests",
    ["method", "endpoint", "status"]
)

QUERY_COUNT = Counter(
    "rag_queries_total",
    "Total RAG queries"
)

# 히스토그램
REQUEST_LATENCY = Histogram(
    "rag_request_latency_seconds",
    "Request latency",
    ["endpoint"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

QUERY_LATENCY = Histogram(
    "rag_query_latency_seconds",
    "RAG query latency",
    buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

# 게이지
DOCUMENT_COUNT = Gauge(
    "rag_document_count",
    "Number of documents"
)

CHUNK_COUNT = Gauge(
    "rag_chunk_count",
    "Number of chunks"
)


def track_request(endpoint: str):
    """요청 추적 데코레이터"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                REQUEST_COUNT.labels(
                    method="POST",
                    endpoint=endpoint,
                    status="success"
                ).inc()
                return result
            except Exception as e:
                REQUEST_COUNT.labels(
                    method="POST",
                    endpoint=endpoint,
                    status="error"
                ).inc()
                raise
            finally:
                REQUEST_LATENCY.labels(endpoint=endpoint).observe(
                    time.time() - start
                )
        return wrapper
    return decorator


def track_query():
    """질의 추적 데코레이터"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            QUERY_COUNT.inc()
            try:
                return func(*args, **kwargs)
            finally:
                QUERY_LATENCY.observe(time.time() - start)
        return wrapper
    return decorator
