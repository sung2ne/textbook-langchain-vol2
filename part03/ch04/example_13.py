def batch_qa(rag, questions, batch_size=5):
    """배치로 질문 처리"""
    results = []
    for i in range(0, len(questions), batch_size):
        batch = questions[i:i + batch_size]
        for q in batch:
            results.append(rag.ask(q))
    return results
