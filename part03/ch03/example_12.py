from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain_ollama import OllamaLLM

# 메타데이터 스키마 정의
metadata_field_info = [
    AttributeInfo(
        name="category",
        description="문서 카테고리 (tutorial, reference, blog)",
        type="string"
    ),
    AttributeInfo(
        name="year",
        description="작성 연도",
        type="integer"
    ),
]

llm = OllamaLLM(model="llama4")

# SelfQueryRetriever 생성
retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_contents="프로그래밍 관련 문서",
    metadata_field_info=metadata_field_info
)

# "2023년에 작성된 튜토리얼 찾아줘"
# → 자동으로 filter={"category": "tutorial", "year": 2023} 적용
results = retriever.invoke("2023년에 작성된 튜토리얼")
