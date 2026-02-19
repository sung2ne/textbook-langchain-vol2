# 기본 추가
collection.add(
    documents=["첫 번째 문서", "두 번째 문서"],
    ids=["id1", "id2"]
)

# 메타데이터와 함께 추가
collection.add(
    documents=["Python 튜토리얼", "JavaScript 가이드"],
    metadatas=[
        {"category": "programming", "lang": "python"},
        {"category": "programming", "lang": "javascript"}
    ],
    ids=["python_doc", "js_doc"]
)

# 임베딩 직접 제공
collection.add(
    documents=["문서 내용"],
    embeddings=[[0.1, 0.2, 0.3, ...]],  # 직접 계산한 벡터
    ids=["custom_embed"]
)
