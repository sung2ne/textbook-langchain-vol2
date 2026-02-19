# 최신 문서 우선
results.sort(key=lambda x: x.metadata.get("created_date", ""), reverse=True)
