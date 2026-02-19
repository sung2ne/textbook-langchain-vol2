from langchain_core.documents import Document

documents = [
    Document(page_content="긴 문서 내용...", metadata={"source": "doc1.txt"}),
    Document(page_content="또 다른 긴 문서...", metadata={"source": "doc2.txt"}),
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

split_docs = splitter.split_documents(documents)

print(f"원본: {len(documents)}개 → 분할 후: {len(split_docs)}개")

# 메타데이터 유지 확인
for doc in split_docs[:3]:
    print(f"출처: {doc.metadata['source']}, 길이: {len(doc.page_content)}")
