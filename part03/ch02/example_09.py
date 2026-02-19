from langchain.text_splitter import Language

# 지원 언어 목록
print([lang.value for lang in Language])
# ['cpp', 'go', 'java', 'kotlin', 'js', 'ts', 'php', 'python', ...]
