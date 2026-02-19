import numpy as np


def compare_models(query, documents, models_dict):
    """모델별 검색 결과 비교"""
    print(f"질문: {query}\n")

    for name, embeddings in models_dict.items():
        print(f"=== {name} ===")

        # 벡터 생성
        query_vec = embeddings.embed_query(query)
        doc_vecs = embeddings.embed_documents(documents)

        # 유사도 계산
        for i, doc in enumerate(documents):
            sim = np.dot(query_vec, doc_vecs[i]) / (
                np.linalg.norm(query_vec) * np.linalg.norm(doc_vecs[i])
            )
            print(f"  [{sim:.3f}] {doc[:30]}...")

        print()


# 비교
models = {
    "nomic-embed-text": OllamaEmbeddings(model="nomic-embed-text"),
    "MiniLM": HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
}

documents = [
    "파이썬으로 웹 개발을 합니다.",
    "LangChain은 AI 앱 프레임워크입니다.",
    "오늘 점심은 김밥입니다.",
]

compare_models("AI 개발 도구", documents, models)
