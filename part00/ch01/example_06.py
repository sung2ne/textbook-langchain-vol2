# 1권 방식: 키워드 검색
def search(query, chunks):
    keywords = query.lower().split()
    results = []
    for chunk in chunks:
        if any(kw in chunk.page_content.lower() for kw in keywords):
            results.append(chunk)
    return results
