from langchain_community.document_loaders import TextLoader

# 단일 파일
loader = TextLoader("./documents/guide.txt", encoding="utf-8")
documents = loader.load()

print(f"로드된 문서 수: {len(documents)}")
print(f"내용 미리보기: {documents[0].page_content[:100]}...")
print(f"메타데이터: {documents[0].metadata}")
