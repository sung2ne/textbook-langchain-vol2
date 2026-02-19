# 대량 문서는 배치로
batch_size = 100
for i in range(0, len(all_documents), batch_size):
    batch = all_documents[i:i + batch_size]
    vectorstore.add_documents(batch)
