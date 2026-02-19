from langchain_community.embeddings import HuggingFaceEmbeddings

# all-MiniLM-L6-v2 (384 차원, 가벼움)
embeddings_mini = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# all-mpnet-base-v2 (768 차원, 고품질)
embeddings_mpnet = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

# 테스트
vec1 = embeddings_mini.embed_query("테스트 문장입니다.")
vec2 = embeddings_mpnet.embed_query("테스트 문장입니다.")

print(f"MiniLM 차원: {len(vec1)}")   # 384
print(f"MPNet 차원: {len(vec2)}")    # 768
