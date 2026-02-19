texts = [
    "오늘 날씨가 좋습니다.",
    "비가 올 것 같습니다.",
    "LangChain 튜토리얼입니다.",
]

metadatas = [
    {"category": "weather"},
    {"category": "weather"},
    {"category": "tech"},
]

vectorstore = FAISS.from_texts(
    texts,
    embeddings,
    metadatas=metadatas
)
