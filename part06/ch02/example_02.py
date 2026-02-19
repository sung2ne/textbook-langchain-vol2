from langchain_ollama import OllamaLLM
from langchain_core.documents import Document
from typing import List, Dict
import json
import re


class SyntheticTestSetGenerator:
    """합성 테스트셋 생성기"""

    def __init__(self, model: str = "llama4"):
        self.llm = OllamaLLM(model=model)

    def generate_questions(self, document: Document, num_questions: int = 3) -> List[Dict]:
        """문서에서 질문 생성"""
        content = document.page_content[:2000]  # 토큰 제한

        prompt = f"""다음 문서를 읽고 {num_questions}개의 질문-답변 쌍을 생성하세요.

문서:
{content}

요구사항:
1. 문서 내용에서 직접 답할 수 있는 질문
2. 다양한 난이도 (쉬움, 보통, 어려움)
3. 구체적이고 명확한 질문

JSON 형식으로 응답하세요:
[
  {{"question": "...", "answer": "...", "difficulty": "easy|medium|hard"}}
]
"""

        response = self.llm.invoke(prompt)

        # JSON 추출
        try:
            # JSON 부분만 추출
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                qa_pairs = json.loads(json_match.group())
                return qa_pairs
        except json.JSONDecodeError:
            pass

        return []

    def generate_from_documents(self, documents: List[Document],
                               questions_per_doc: int = 2) -> List[Dict]:
        """여러 문서에서 테스트셋 생성"""
        all_qa_pairs = []

        for doc in documents:
            qa_pairs = self.generate_questions(doc, questions_per_doc)

            for qa in qa_pairs:
                qa["source"] = doc.metadata.get("source", "unknown")
                qa["doc_id"] = doc.metadata.get("doc_id", "unknown")

            all_qa_pairs.extend(qa_pairs)

        return all_qa_pairs


# 사용
generator = SyntheticTestSetGenerator()

# 샘플 문서
documents = [
    Document(
        page_content="""LangChain은 LLM 애플리케이션 개발을 위한 프레임워크입니다.
        주요 컴포넌트로는 모델, 프롬프트, 체인, 에이전트가 있습니다.
        체인은 여러 컴포넌트를 연결하여 복잡한 작업을 수행합니다.""",
        metadata={"source": "langchain_intro.md", "doc_id": "doc_001"}
    ),
    Document(
        page_content="""RAG는 Retrieval-Augmented Generation의 약자입니다.
        외부 지식을 검색하여 LLM의 답변 품질을 높입니다.
        환각을 줄이고 최신 정보를 반영할 수 있습니다.""",
        metadata={"source": "rag_basics.md", "doc_id": "doc_002"}
    )
]

qa_pairs = generator.generate_from_documents(documents, questions_per_doc=2)

print(f"생성된 Q&A 쌍: {len(qa_pairs)}개")
for qa in qa_pairs:
    print(f"\nQ: {qa.get('question', 'N/A')}")
    print(f"A: {qa.get('answer', 'N/A')}")
