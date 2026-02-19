from langchain_ollama import OllamaEmbeddings

# 기본 설정
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 상세 설정
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434",  # Ollama 서버 주소
    num_ctx=8192,                       # 컨텍스트 크기
)

# 사용
text = "LangChain은 LLM 프레임워크입니다."
vector = embeddings.embed_query(text)
print(f"차원: {len(vector)}")  # 768
