from langchain_community.vectorstores import Weaviate
from langchain_ollama import OllamaEmbeddings
import weaviate

# 클라이언트 연결
client = weaviate.Client(url="http://localhost:8080")

embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 벡터 저장소 생성
vectorstore = Weaviate.from_texts(
    texts=["문서 1", "문서 2"],
    embedding=embeddings,
    client=client,
    index_name="Documents"
)

# 검색
results = vectorstore.similarity_search("검색어")
