from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama4")
prompt = ChatPromptTemplate.from_template("{question}")
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"question": "안녕하세요"})
