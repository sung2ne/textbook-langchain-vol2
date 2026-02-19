from langchain_community.document_loaders import WebBaseLoader

# 단일 URL
loader = WebBaseLoader("https://example.com/article")
documents = loader.load()

# 여러 URL
loader = WebBaseLoader([
    "https://example.com/page1",
    "https://example.com/page2",
])
documents = loader.load()

for doc in documents:
    print(f"URL: {doc.metadata['source']}")
    print(f"내용: {doc.page_content[:100]}...")
