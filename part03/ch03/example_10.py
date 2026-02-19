from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama4")

# 압축기 생성
compressor = LLMChainExtractor.from_llm(llm)

# 압축 Retriever
retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever()
)

# 검색 결과에서 질문 관련 부분만 추출
results = retriever.invoke("파이썬 설치 방법")

# 원본: "파이썬은 1991년에 만들어졌습니다. 설치는 python.org에서..."
# 압축: "설치는 python.org에서 다운로드하여 진행합니다."
