class VectorStoreMigrator:
    """벡터 저장소 마이그레이션"""

    @staticmethod
    def migrate(source, target, batch_size=100):
        """소스에서 타겟으로 마이그레이션"""
        # 소스에서 모든 문서 가져오기
        all_docs = source.get()  # ChromaDB의 경우

        # 배치로 타겟에 추가
        for i in range(0, len(all_docs["documents"]), batch_size):
            batch_docs = []
            for j in range(i, min(i + batch_size, len(all_docs["documents"]))):
                doc = Document(
                    page_content=all_docs["documents"][j],
                    metadata=all_docs["metadatas"][j] if all_docs["metadatas"] else {}
                )
                batch_docs.append(doc)

            target.add_documents(batch_docs)
            print(f"마이그레이션: {i + len(batch_docs)}/{len(all_docs['documents'])}")

        return len(all_docs["documents"])
