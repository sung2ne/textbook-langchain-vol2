from langchain_community.document_loaders import CSVLoader

# 기본 로딩 (각 행이 하나의 문서)
loader = CSVLoader("./data/products.csv")
documents = loader.load()

# 특정 컬럼만 내용으로
loader = CSVLoader(
    "./data/products.csv",
    source_column="product_name",
    csv_args={"delimiter": ","}
)
documents = loader.load()

print(f"총 {len(documents)}개 문서")
