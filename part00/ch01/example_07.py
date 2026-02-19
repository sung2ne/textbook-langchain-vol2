# 2권 방식: 벡터 검색 (의미 기반)
results = vectorstore.similarity_search("LangChain이 뭐야?", k=3)
# "LangChain 소개", "LangChain 개념", "LangChain 정의" 등 모두 찾음
