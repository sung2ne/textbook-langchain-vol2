class EmbeddingFactory:
    @staticmethod
    def create(model_type: str, **kwargs):
        """임베딩 모델 생성"""
        if model_type == "ollama":
            from langchain_ollama import OllamaEmbeddings
            model = kwargs.get("model", "nomic-embed-text")
            return OllamaEmbeddings(model=model)

        elif model_type == "huggingface":
            from langchain_community.embeddings import HuggingFaceEmbeddings
            model = kwargs.get("model", "sentence-transformers/all-MiniLM-L6-v2")
            return HuggingFaceEmbeddings(model_name=model)

        elif model_type == "openai":
            from langchain_openai import OpenAIEmbeddings
            model = kwargs.get("model", "text-embedding-3-small")
            return OpenAIEmbeddings(model=model)

        else:
            raise ValueError(f"Unknown model type: {model_type}")


# 사용
embeddings = EmbeddingFactory.create("ollama", model="nomic-embed-text")
# embeddings = EmbeddingFactory.create("huggingface")
# embeddings = EmbeddingFactory.create("openai")

vec = embeddings.embed_query("테스트")
print(f"차원: {len(vec)}")
