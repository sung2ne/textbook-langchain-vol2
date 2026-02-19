from langchain_community.document_loaders import DirectoryLoader, TextLoader

# 폴더의 모든 txt 파일
loader = DirectoryLoader(
    "./documents",
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)

documents = loader.load()
print(f"총 {len(documents)}개 문서 로드")

for doc in documents:
    print(f"- {doc.metadata['source']}")
