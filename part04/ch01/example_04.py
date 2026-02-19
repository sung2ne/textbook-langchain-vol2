import logging

# 로깅으로 생성된 쿼리 확인
logging.basicConfig(level=logging.INFO)
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.DEBUG)

results = retriever.invoke("RAG 작동 원리")
# 로그에 생성된 쿼리들이 출력됨
