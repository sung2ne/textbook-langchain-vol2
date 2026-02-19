from langchain_community.document_loaders import PyPDFDirectoryLoader

loader = PyPDFDirectoryLoader("./pdf_documents")
documents = loader.load()

print(f"총 {len(documents)}개 페이지 로드")
