from dotenv import load_dotenv
import os

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL", "llama4")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
