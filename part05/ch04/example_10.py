from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama4")
response = llm.invoke("안녕하세요")
print(response)
