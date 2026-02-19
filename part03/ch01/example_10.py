from langchain_community.document_loaders import UnstructuredMarkdownLoader

loader = UnstructuredMarkdownLoader("./docs/README.md")
documents = loader.load()

print(documents[0].page_content[:200])
