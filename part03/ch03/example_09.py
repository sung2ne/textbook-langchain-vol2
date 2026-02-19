from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama4")

# 기본 retriever
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# MultiQueryRetriever
retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=llm
)

# "파이썬 배우기" →
#   1. "파이썬 프로그래밍 입문"
#   2. "Python 학습 방법"
#   3. "파이썬 시작하기 튜토리얼"
# 각각 검색 후 결과 통합

results = retriever.invoke("파이썬 배우기")
