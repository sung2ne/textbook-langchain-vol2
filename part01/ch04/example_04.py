from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

# 기본 임베딩
base_embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 캐시 저장소
cache_store = LocalFileStore("./embedding_cache")

# 캐시 적용 임베딩
cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=base_embeddings,
    document_embedding_cache=cache_store,
    namespace="nomic"  # 모델별 네임스페이스
)

# 첫 번째 호출 - 실제 임베딩 생성 (느림)
texts = ["문서 1", "문서 2", "문서 3"]
vectors1 = cached_embeddings.embed_documents(texts)
print("첫 번째 호출 완료")

# 두 번째 호출 - 캐시에서 로드 (빠름)
vectors2 = cached_embeddings.embed_documents(texts)
print("두 번째 호출 완료 (캐시)")
