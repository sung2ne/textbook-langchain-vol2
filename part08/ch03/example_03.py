# app/services/chain_service.py
from typing import List, Generator
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from app.config import settings


# 프롬프트 템플릿
QA_PROMPT = PromptTemplate(
    template="""다음 컨텍스트를 바탕으로 질문에 답하세요.
답변할 수 없는 경우 "정보가 부족합니다"라고 말하세요.

컨텍스트:
{context}

질문: {question}

답변:""",
    input_variables=["context", "question"]
)


SUMMARY_PROMPT = PromptTemplate(
    template="""다음 문서들을 요약하세요.

문서:
{documents}

요약:""",
    input_variables=["documents"]
)


class ChainService:
    """LLM 체인 서비스"""

    def __init__(self):
        self.llm = OllamaLLM(model=settings.llm_model)

    def answer(self, question: str, contexts: List[Document]) -> str:
        """답변 생성"""
        # 컨텍스트 구성
        context_text = "\n\n".join(
            f"[{i+1}] {doc.page_content}"
            for i, doc in enumerate(contexts)
        )

        # 프롬프트 생성
        prompt = QA_PROMPT.format(
            context=context_text,
            question=question
        )

        # 답변 생성
        return self.llm.invoke(prompt)

    def stream_answer(self, question: str,
                     contexts: List[Document]) -> Generator[str, None, None]:
        """스트리밍 답변"""
        context_text = "\n\n".join(
            f"[{i+1}] {doc.page_content}"
            for i, doc in enumerate(contexts)
        )

        prompt = QA_PROMPT.format(
            context=context_text,
            question=question
        )

        for chunk in self.llm.stream(prompt):
            yield chunk

    def summarize(self, documents: List[Document]) -> str:
        """문서 요약"""
        doc_text = "\n\n---\n\n".join(
            doc.page_content for doc in documents
        )

        prompt = SUMMARY_PROMPT.format(documents=doc_text)
        return self.llm.invoke(prompt)
