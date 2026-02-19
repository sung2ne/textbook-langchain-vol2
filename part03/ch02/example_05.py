from langchain.text_splitter import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=100,      # 토큰 수
    chunk_overlap=10,
)

chunks = splitter.split_text(text)
