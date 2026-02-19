# 스트림으로 실행
for chunk in rag_chain.stream("LangChain 설명해줘"):
    print(chunk, end="", flush=True)
