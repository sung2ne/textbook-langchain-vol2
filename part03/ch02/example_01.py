from langchain.text_splitter import CharacterTextSplitter

text = """파이썬은 1991년에 만들어진 프로그래밍 언어입니다.

파이썬의 특징은 간결한 문법입니다. 들여쓰기로 코드 블록을 구분합니다.

파이썬은 데이터 분석, 웹 개발, 인공지능 등 다양한 분야에서 사용됩니다."""

splitter = CharacterTextSplitter(
    separator="\n\n",   # 분할 기준
    chunk_size=100,     # 청크 크기 (문자 수)
    chunk_overlap=20,   # 청크 간 겹침
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks):
    print(f"청크 {i+1}: {chunk[:50]}...")
