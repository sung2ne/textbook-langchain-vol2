from langchain_ollama import OllamaLLM
from langchain_core.documents import Document
from typing import List, Dict
from enum import Enum


class QuestionType(Enum):
    FACTUAL = "factual"        # 사실 확인
    COMPARISON = "comparison"   # 비교
    REASONING = "reasoning"     # 추론
    PROCEDURAL = "procedural"   # 절차/방법
    DEFINITION = "definition"   # 정의


class DiverseQuestionGenerator:
    """다양한 유형의 질문 생성기"""

    def __init__(self, model: str = "llama4"):
        self.llm = OllamaLLM(model=model)

        self.type_prompts = {
            QuestionType.FACTUAL: "사실을 확인하는 질문 (누가, 무엇을, 언제, 어디서)",
            QuestionType.COMPARISON: "비교하는 질문 (A와 B의 차이점)",
            QuestionType.REASONING: "이유나 원인을 묻는 질문 (왜, 어떻게)",
            QuestionType.PROCEDURAL: "절차나 방법을 묻는 질문 (어떻게 하는지)",
            QuestionType.DEFINITION: "정의나 개념을 묻는 질문 (~이란 무엇인가)"
        }

    def generate_by_type(self, document: Document,
                        question_type: QuestionType) -> Dict:
        """유형별 질문 생성"""
        content = document.page_content[:1500]
        type_desc = self.type_prompts[question_type]

        prompt = f"""다음 문서를 읽고 "{type_desc}" 유형의 질문-답변을 1개 생성하세요.

문서:
{content}

JSON 형식으로 응답하세요:
{{"question": "...", "answer": "..."}}
"""

        response = self.llm.invoke(prompt)

        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                qa = json.loads(json_match.group())
                qa["type"] = question_type.value
                qa["source"] = document.metadata.get("source", "unknown")
                return qa
        except:
            pass

        return {"question": "", "answer": "", "type": question_type.value}

    def generate_diverse(self, document: Document) -> List[Dict]:
        """모든 유형의 질문 생성"""
        qa_pairs = []

        for q_type in QuestionType:
            qa = self.generate_by_type(document, q_type)
            if qa.get("question"):
                qa_pairs.append(qa)

        return qa_pairs


# 사용
generator = DiverseQuestionGenerator()

doc = Document(
    page_content="""ChromaDB는 오픈소스 벡터 데이터베이스입니다.
    임베딩을 저장하고 유사도 검색을 수행합니다.
    파일 기반과 클라이언트-서버 모드를 지원합니다.
    FAISS와 달리 메타데이터 필터링이 기본 지원됩니다.
    설치는 pip install chromadb로 가능합니다.""",
    metadata={"source": "chromadb.md"}
)

qa_pairs = generator.generate_diverse(doc)

print("=== 다양한 유형의 질문 ===")
for qa in qa_pairs:
    print(f"\n[{qa.get('type', 'unknown')}]")
    print(f"Q: {qa.get('question', 'N/A')}")
    print(f"A: {qa.get('answer', 'N/A')}")
