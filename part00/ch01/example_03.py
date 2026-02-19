from langchain_core.output_parsers import JsonOutputParser

chain = prompt | llm | JsonOutputParser()
