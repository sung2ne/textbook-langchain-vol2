# 공통 인터페이스
vectorstore.add_documents(documents)      # 문서 추가
vectorstore.similarity_search(query)      # 유사 검색
vectorstore.similarity_search_with_score(query)  # 점수 포함 검색
vectorstore.as_retriever()                # Retriever로 변환
