from langchain_ollama import OllamaLLM
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


# 기본 스트리밍
llm = OllamaLLM(model="llama4")

# stream 메서드 사용
for chunk in llm.stream("LangChain이란 무엇인가요?"):
    print(chunk, end="", flush=True)


# 콜백 사용
llm_with_callback = OllamaLLM(
    model="llama4",
    callbacks=[StreamingStdOutCallbackHandler()]
)

response = llm_with_callback.invoke("LangChain이란?")
