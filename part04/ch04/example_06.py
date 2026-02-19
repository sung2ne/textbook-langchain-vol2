import yaml


class ConfigurableSearchPipeline:
    """설정 파일 기반 파이프라인"""

    DEFAULT_CONFIG = {
        "embedding_model": "nomic-embed-text",
        "llm_model": "llama4",
        "reranker_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
        "default_strategy": {
            "use_hybrid": True,
            "use_reranking": True,
            "bm25_weight": 0.5,
            "initial_k": 20,
            "final_k": 5
        }
    }

    def __init__(self, config_path: str = None):
        if config_path:
            with open(config_path, "r") as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = self.DEFAULT_CONFIG

    def _create_pipeline(self, documents: List[Document]):
        """설정에 따른 파이프라인 생성"""
        # 설정 기반 컴포넌트 초기화
        embeddings = OllamaEmbeddings(model=self.config["embedding_model"])
        # ... 나머지 초기화

    def save_config(self, path: str):
        """현재 설정 저장"""
        with open(path, "w") as f:
            yaml.dump(self.config, f)
