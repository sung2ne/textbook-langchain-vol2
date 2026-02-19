# Ollama 임베딩 함수 (커스텀)
from langchain_ollama import OllamaEmbeddings


class OllamaEmbeddingFunction:
    def __init__(self, model="nomic-embed-text"):
        self.embeddings = OllamaEmbeddings(model=model)

    def __call__(self, input):
        return self.embeddings.embed_documents(input)


# 사용
ollama_ef = OllamaEmbeddingFunction()
collection = client.create_collection(
    name="ollama_collection",
    embedding_function=ollama_ef
)
