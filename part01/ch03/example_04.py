from langchain_openai import OpenAIEmbeddings
import os

os.environ["OPENAI_API_KEY"] = "your_api_key"

# text-embedding-3-small
embeddings_small = OpenAIEmbeddings(model="text-embedding-3-small")

# text-embedding-3-large (더 고품질)
embeddings_large = OpenAIEmbeddings(model="text-embedding-3-large")

vec = embeddings_small.embed_query("테스트")
print(f"OpenAI 차원: {len(vec)}")  # 1536
