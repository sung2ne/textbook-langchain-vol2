import time


def benchmark_embedding(name, embeddings, texts, iterations=10):
    """임베딩 속도 측정"""
    times = []

    for _ in range(iterations):
        start = time.time()
        embeddings.embed_documents(texts)
        times.append(time.time() - start)

    avg_time = sum(times) / len(times)
    print(f"{name}: 평균 {avg_time:.3f}초 ({len(texts)}개 문서)")


# 테스트 문서
texts = [f"테스트 문서 {i}입니다." for i in range(10)]

benchmark_embedding("nomic", embeddings_nomic, texts)
benchmark_embedding("MiniLM", embeddings_mini, texts)
