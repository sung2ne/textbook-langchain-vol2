from langchain_core.documents import Document

doc = Document(
    page_content="문서의 실제 내용입니다.",
    metadata={
        "source": "example.txt",
        "page": 1,
        "author": "홍길동"
    }
)

print(doc.page_content)  # 내용
print(doc.metadata)      # 메타데이터
