from collections import defaultdict


class MetadataIndex:
    """메타데이터 인덱스"""

    def __init__(self):
        self.indices = defaultdict(lambda: defaultdict(list))

    def add_document(self, doc_id: str, metadata: dict):
        """문서 메타데이터 인덱싱"""
        for key, value in metadata.items():
            self.indices[key][value].append(doc_id)

    def query(self, **filters) -> set:
        """필터 조건으로 문서 ID 조회"""
        result_sets = []

        for key, value in filters.items():
            if key in self.indices and value in self.indices[key]:
                result_sets.append(set(self.indices[key][value]))
            else:
                return set()

        if not result_sets:
            return set()

        return set.intersection(*result_sets)

    def get_unique_values(self, field: str) -> List:
        """필드의 고유 값 조회"""
        return list(self.indices.get(field, {}).keys())


# 사용
index = MetadataIndex()

for i, doc in enumerate(docs):
    index.add_document(f"doc_{i}", doc.metadata)

# 조회
matching_ids = index.query(level=2)
print(f"레벨 2 문서: {matching_ids}")

# 고유 값 확인
print(f"섹션 레벨: {index.get_unique_values('level')}")
