# 질문 임베딩 (검색할 때)
query_vector = embeddings.embed_query("LangChain이 뭐야?")

# 문서 임베딩 (저장할 때)
doc_vectors = embeddings.embed_documents([
    "LangChain은 LLM 프레임워크입니다.",
    "Python으로 AI 앱을 만들 수 있습니다."
])
