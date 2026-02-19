class MultiLevelChunker:
    """다중 레벨 청킹"""

    def __init__(self, levels: List[int] = None):
        """
        levels: 각 레벨의 청크 크기 [2000, 500, 100]
        """
        self.levels = levels or [2000, 500, 100]
        self.splitters = [
            RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=size // 10)
            for size in self.levels
        ]

    def split(self, documents: List[Document]) -> Dict[int, List[Document]]:
        """다중 레벨 분할"""
        result = {}

        for level, splitter in enumerate(self.splitters):
            if level == 0:
                # 첫 레벨: 원본에서 분할
                chunks = splitter.split_documents(documents)
            else:
                # 이후 레벨: 이전 레벨에서 분할
                chunks = splitter.split_documents(result[level - 1])

            # 메타데이터 추가
            for i, chunk in enumerate(chunks):
                chunk.metadata["level"] = level
                chunk.metadata[f"level_{level}_index"] = i

            result[level] = chunks

        return result


# 사용
multi_chunker = MultiLevelChunker(levels=[1000, 300, 100])
levels = multi_chunker.split(documents)

print("레벨별 청크 수:")
for level, chunks in levels.items():
    print(f"  레벨 {level}: {len(chunks)}개 (크기: {multi_chunker.levels[level]})")
