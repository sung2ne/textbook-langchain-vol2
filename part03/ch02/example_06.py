from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base",  # GPT-4 인코딩
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(text)
