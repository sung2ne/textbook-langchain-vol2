from langchain_community.embeddings import HuggingFaceEmbeddings

# 기본 설정
embeddings = HuggingFaceEmbeddings()  # 기본 모델 사용

# 모델 지정
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": "cpu"},  # GPU: "cuda"
    encode_kwargs={"normalize_embeddings": True}  # 정규화
)

# 캐시 설정 (모델 다운로드 위치)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    cache_folder="./models"  # 커스텀 캐시 폴더
)

vector = embeddings.embed_query("테스트")
print(f"차원: {len(vector)}")
