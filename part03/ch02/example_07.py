from langchain.text_splitter import MarkdownTextSplitter

markdown_text = """
# 제목

## 소제목 1
내용입니다.

## 소제목 2
또 다른 내용입니다.

### 하위 섹션
상세 내용입니다.
"""

splitter = MarkdownTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)

chunks = splitter.split_text(markdown_text)

for i, chunk in enumerate(chunks):
    print(f"--- 청크 {i+1} ---")
    print(chunk)
