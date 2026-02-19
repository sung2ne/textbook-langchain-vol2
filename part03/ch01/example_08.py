from langchain_community.document_loaders import JSONLoader


# jq 스키마로 데이터 추출
loader = JSONLoader(
    file_path="./data/articles.json",
    jq_schema=".articles[]",
    text_content=False
)
documents = loader.load()
