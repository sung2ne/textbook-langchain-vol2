from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import time


class BatchEvaluator:
    """배치 평가기"""

    def __init__(self, rag_system, max_workers: int = 4):
        self.rag_system = rag_system
        self.max_workers = max_workers

    def evaluate_single(self, case: Dict) -> Dict:
        """단일 케이스 평가"""
        question = case["question"]

        start = time.time()
        response = self.rag_system(question)
        latency = time.time() - start

        return {
            "question": question,
            "expected": case.get("ground_truth", ""),
            "actual": response.get("answer", ""),
            "retrieved_docs": response.get("retrieved_docs", []),
            "relevant_docs": case.get("relevant_doc_ids", []),
            "latency": latency
        }

    def evaluate_batch(self, test_cases: List[Dict],
                      progress_callback=None) -> List[Dict]:
        """병렬 배치 평가"""
        results = []
        completed = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.evaluate_single, case): i
                for i, case in enumerate(test_cases)
            }

            for future in as_completed(futures):
                result = future.result()
                results.append(result)

                completed += 1
                if progress_callback:
                    progress_callback(completed, len(test_cases))

        return results

    def evaluate_with_retry(self, test_cases: List[Dict],
                           max_retries: int = 3) -> List[Dict]:
        """재시도 포함 평가"""
        results = []
        failed = []

        for case in test_cases:
            for attempt in range(max_retries):
                try:
                    result = self.evaluate_single(case)
                    results.append(result)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        failed.append({
                            "case": case,
                            "error": str(e)
                        })

        return {"results": results, "failed": failed}


# 사용
batch_evaluator = BatchEvaluator(mock_rag_system, max_workers=4)

test_cases = [{"question": f"Q{i}?", "ground_truth": f"A{i}"} for i in range(10)]

def progress(done, total):
    print(f"진행: {done}/{total}")

results = batch_evaluator.evaluate_batch(test_cases, progress_callback=progress)
print(f"완료: {len(results)}개")
