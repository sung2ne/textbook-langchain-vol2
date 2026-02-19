# FAISS - 빠른 검색
vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local("./faiss_index")
