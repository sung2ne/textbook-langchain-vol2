from langchain_community.embeddings import HuggingFaceEmbeddings, OllamaEmbeddings
from typing import List, Dict


class EmbeddingExperiment:
    """임베딩 모델 실험"""

    def __init__(self):
        self.models = {
            "nomic": OllamaEmbeddings(model="nomic-embed-text"),
            "bge-small": HuggingFaceEmbeddings(
                model_name="BAAI/bge-small-en-v1.5"
            ),
            "multilingual": HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
            )
        }

    def evaluate_model(self, model_name: str, queries: List[str],
                      documents: List[str], relevant_pairs: List[tuple]) -> Dict:
        """모델 평가"""
        embeddings = self.models.get(model_name)
        if not embeddings:
            return {"error": f"Unknown model: {model_name}"}

        # 문서 임베딩
        doc_embeddings = embeddings.embed_documents(documents)

        # 쿼리별 검색 및 평가
        hits = 0
        total = len(relevant_pairs)

        for query_idx, doc_idx in relevant_pairs:
            query_emb = embeddings.embed_query(queries[query_idx])

            # 가장 유사한 문서 찾기
            import numpy as np
            similarities = [
                np.dot(query_emb, doc_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb))
                for doc_emb in doc_embeddings
            ]

            top_idx = np.argmax(similarities)
            if top_idx == doc_idx:
                hits += 1

        return {
            "model": model_name,
            "accuracy": hits / total if total > 0 else 0
        }

    def compare_all(self, queries: List[str], documents: List[str],
                   relevant_pairs: List[tuple]) -> List[Dict]:
        """모든 모델 비교"""
        results = []

        for name in self.models:
            result = self.evaluate_model(name, queries, documents, relevant_pairs)
            results.append(result)
            print(f"{name}: {result.get('accuracy', 0):.2%}")

        return results


# 사용
experiment = EmbeddingExperiment()

queries = ["LangChain 설치 방법", "벡터 DB 종류"]
documents = ["pip install langchain으로 설치합니다.", "ChromaDB, FAISS, Pinecone이 있습니다."]
relevant_pairs = [(0, 0), (1, 1)]  # (쿼리 인덱스, 문서 인덱스)

# results = experiment.compare_all(queries, documents, relevant_pairs)
