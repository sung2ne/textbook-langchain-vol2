from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict


class ChunkingExperiment:
    """청킹 전략 실험"""

    def __init__(self):
        self.strategies = {
            "small": {"chunk_size": 200, "overlap": 20},
            "medium": {"chunk_size": 500, "overlap": 50},
            "large": {"chunk_size": 1000, "overlap": 100}
        }

    def split_with_strategy(self, text: str, strategy: str) -> List[str]:
        """전략별 분할"""
        config = self.strategies.get(strategy, self.strategies["medium"])

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config["chunk_size"],
            chunk_overlap=config["overlap"]
        )

        return splitter.split_text(text)

    def analyze_chunks(self, text: str, strategy: str) -> Dict:
        """청크 분석"""
        chunks = self.split_with_strategy(text, strategy)

        lengths = [len(c) for c in chunks]

        return {
            "strategy": strategy,
            "num_chunks": len(chunks),
            "avg_length": sum(lengths) / len(lengths) if lengths else 0,
            "min_length": min(lengths) if lengths else 0,
            "max_length": max(lengths) if lengths else 0
        }

    def compare_strategies(self, text: str) -> List[Dict]:
        """전략 비교"""
        results = []

        for strategy in self.strategies:
            result = self.analyze_chunks(text, strategy)
            results.append(result)

        return results


# 사용
chunking_exp = ChunkingExperiment()

sample_text = "LangChain은 LLM 프레임워크입니다. " * 100

results = chunking_exp.compare_strategies(sample_text)
for r in results:
    print(f"{r['strategy']}: {r['num_chunks']}청크, 평균 {r['avg_length']:.0f}자")
