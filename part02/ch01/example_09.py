import chromadb
from chromadb.utils import embedding_functions

# Sentence Transformers 임베딩
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# 컬렉션에 적용
collection = client.create_collection(
    name="custom_embeddings",
    embedding_function=sentence_transformer_ef
)
