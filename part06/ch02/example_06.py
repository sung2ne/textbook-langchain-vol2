from langchain_ollama import OllamaLLM
from langchain_core.documents import Document
from typing import List, Dict
import json
from pathlib import Path


class TestSetPipeline:
    """완전한 테스트셋 파이프라인"""

    def __init__(self, output_dir: str = "./test_sets"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.generator = SyntheticTestSetGenerator()
        self.validator = TestSetValidator()
        self.splitter = TestSetSplitter()

    def generate(self, documents: List[Document],
                questions_per_doc: int = 3) -> List[Dict]:
        """테스트셋 생성"""
        print(f"📝 {len(documents)}개 문서에서 테스트셋 생성 중...")

        qa_pairs = self.generator.generate_from_documents(
            documents, questions_per_doc
        )

        print(f"   → {len(qa_pairs)}개 Q&A 생성됨")
        return qa_pairs

    def validate(self, test_cases: List[Dict]) -> Dict:
        """검증"""
        print("🔍 테스트셋 검증 중...")

        result = self.validator.validate_test_set(test_cases)

        print(f"   → 유효: {result['valid_cases']}/{result['total_cases']}")
        print(f"   → 평균 점수: {result['average_score']:.2f}")

        return result

    def filter_valid(self, test_cases: List[Dict],
                    min_score: float = 0.7) -> List[Dict]:
        """유효한 케이스만 필터"""
        filtered = []

        for case in test_cases:
            result = self.validator.validate_case(case)
            if result.score >= min_score:
                filtered.append(case)

        print(f"🔽 {len(test_cases)} → {len(filtered)}개로 필터링")
        return filtered

    def split_and_save(self, test_cases: List[Dict], name: str):
        """분할 및 저장"""
        train, val, test = self.splitter.split(test_cases)

        # 저장
        for split_name, data in [("train", train), ("val", val), ("test", test)]:
            path = self.output_dir / f"{name}_{split_name}.json"

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"💾 {path.name}: {len(data)}개")

        return {"train": train, "val": val, "test": test}

    def run(self, documents: List[Document], name: str,
           questions_per_doc: int = 3, min_score: float = 0.7) -> Dict:
        """전체 파이프라인 실행"""
        print("=" * 50)
        print(f"테스트셋 파이프라인: {name}")
        print("=" * 50)

        # 1. 생성
        qa_pairs = self.generate(documents, questions_per_doc)

        # 2. 검증
        validation = self.validate(qa_pairs)

        # 3. 필터링
        filtered = self.filter_valid(qa_pairs, min_score)

        # 4. 분할 및 저장
        splits = self.split_and_save(filtered, name)

        # 5. 리포트
        print("\n" + "=" * 50)
        print("완료!")
        print(f"  총 생성: {len(qa_pairs)}개")
        print(f"  필터 후: {len(filtered)}개")
        print(f"  Train/Val/Test: {len(splits['train'])}/{len(splits['val'])}/{len(splits['test'])}")

        return {
            "generated": qa_pairs,
            "filtered": filtered,
            "splits": splits,
            "validation": validation
        }


# 사용
pipeline = TestSetPipeline()

# 문서 준비
documents = [
    Document(
        page_content="LangChain은 LLM 프레임워크입니다. 체인, 에이전트, 도구를 제공합니다.",
        metadata={"source": "intro.md", "doc_id": "doc_001"}
    ),
    Document(
        page_content="ChromaDB는 벡터 데이터베이스입니다. 임베딩 저장과 검색을 지원합니다.",
        metadata={"source": "chromadb.md", "doc_id": "doc_002"}
    )
]

# 파이프라인 실행
result = pipeline.run(
    documents=documents,
    name="langchain_test",
    questions_per_doc=2,
    min_score=0.6
)
