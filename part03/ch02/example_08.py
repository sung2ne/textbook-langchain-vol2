from langchain.text_splitter import Language, RecursiveCharacterTextSplitter

# Python 코드 분할
python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=500,
    chunk_overlap=50
)

python_code = """
def hello():
    print("Hello, World!")

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b
"""

chunks = python_splitter.split_text(python_code)
