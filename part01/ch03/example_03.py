# 한국어 임베딩 모델
embeddings_ko = HuggingFaceEmbeddings(
    model_name="jhgan/ko-sroberta-multitask"
)

vec = embeddings_ko.embed_query("안녕하세요, 한국어 테스트입니다.")
print(f"한국어 모델 차원: {len(vec)}")  # 768
