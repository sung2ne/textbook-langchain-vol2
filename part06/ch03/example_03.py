from typing import List, Dict
import statistics
import time


class PerformanceBenchmark:
    """성능 벤치마크"""

    def __init__(self, rag_system):
        self.rag_system = rag_system

    def measure_latency(self, questions: List[str],
                       warmup_runs: int = 3) -> Dict:
        """지연 시간 측정"""
        # 워밍업
        for _ in range(warmup_runs):
            self.rag_system(questions[0])

        latencies = []

        for question in questions:
            start = time.time()
            self.rag_system(question)
            latency = time.time() - start
            latencies.append(latency)

        return {
            "count": len(latencies),
            "mean": statistics.mean(latencies),
            "median": statistics.median(latencies),
            "stdev": statistics.stdev(latencies) if len(latencies) > 1 else 0,
            "min": min(latencies),
            "max": max(latencies),
            "p90": self._percentile(latencies, 90),
            "p99": self._percentile(latencies, 99)
        }

    def _percentile(self, data: List[float], percentile: int) -> float:
        """백분위수 계산"""
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]

    def measure_throughput(self, questions: List[str],
                          duration_seconds: int = 60) -> Dict:
        """처리량 측정"""
        count = 0
        errors = 0
        start = time.time()

        while time.time() - start < duration_seconds:
            try:
                question = questions[count % len(questions)]
                self.rag_system(question)
                count += 1
            except Exception:
                errors += 1

        elapsed = time.time() - start

        return {
            "total_requests": count,
            "errors": errors,
            "duration_seconds": elapsed,
            "requests_per_second": count / elapsed,
            "error_rate": errors / max(count + errors, 1)
        }


# 사용
benchmark = PerformanceBenchmark(mock_rag_system)

questions = [f"질문 {i}?" for i in range(20)]

# 지연 시간
latency = benchmark.measure_latency(questions)
print("=== 지연 시간 ===")
print(f"평균: {latency['mean']*1000:.1f}ms")
print(f"P90: {latency['p90']*1000:.1f}ms")
print(f"P99: {latency['p99']*1000:.1f}ms")

# 처리량 (짧은 테스트)
throughput = benchmark.measure_throughput(questions, duration_seconds=5)
print("\n=== 처리량 ===")
print(f"RPS: {throughput['requests_per_second']:.1f}")
print(f"에러율: {throughput['error_rate']:.2%}")
