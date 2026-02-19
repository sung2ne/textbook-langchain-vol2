from langchain_community.document_loaders import PyPDFLoader

# PDF 로드 (페이지별)
loader = PyPDFLoader("./documents/manual.pdf")
pages = loader.load()

print(f"총 {len(pages)} 페이지")

for page in pages[:3]:
    print(f"페이지 {page.metadata['page']}: {page.page_content[:50]}...")
