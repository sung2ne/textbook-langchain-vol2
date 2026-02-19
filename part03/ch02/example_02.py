from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " ", ""]
)

# 분할 순서:
# 1. 먼저 \n\n (단락)으로 분할 시도
# 2. 너무 크면 \n (줄바꿈)으로 분할
# 3. 여전히 크면 . (문장)으로 분할
# 4. 계속해서 더 작은 단위로...
