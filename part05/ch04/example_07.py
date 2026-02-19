from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.documents import Document
from typing import List, Dict
from pathlib import Path


class IntegratedMultimodalRAG:
    """통합 멀티모달 RAG 시스템"""

    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.llm = OllamaLLM(model="llama4")
        self.vectorstore = None
        self.image_describer = CachedImageDescriber()
        self.documents: List[Document] = []

    def add_text_document(self, content: str, source: str):
        """텍스트 문서 추가"""
        doc = Document(
            page_content=content,
            metadata={"source": source, "type": "text"}
        )
        self.documents.append(doc)

    def add_image_document(self, image_path: str):
        """이미지 문서 추가"""
        # 이미지 설명 생성
        description = self.image_describer.describe(image_path)

        doc = Document(
            page_content=description,
            metadata={
                "source": image_path,
                "type": "image",
                "image_path": image_path
            }
        )
        self.documents.append(doc)

    def add_pdf(self, pdf_path: str):
        """PDF 추가 (텍스트 + 이미지)"""
        loader = MultimodalPDFLoader()
        pdf_docs = loader.load(pdf_path)

        for doc in pdf_docs:
            if doc.metadata.get("type") == "image":
                # 이미지 설명 추가
                image_path = doc.metadata.get("image_path")
                if image_path:
                    description = self.image_describer.describe(image_path)
                    doc.page_content = description

            self.documents.append(doc)

    def build_index(self):
        """벡터 인덱스 구축"""
        if not self.documents:
            raise ValueError("문서가 없습니다.")

        self.vectorstore = Chroma.from_documents(
            self.documents,
            self.embeddings
        )

    def query(self, question: str, k: int = 5) -> Dict:
        """질문에 답변"""
        if self.vectorstore is None:
            raise ValueError("인덱스가 구축되지 않았습니다.")

        # 관련 문서 검색
        results = self.vectorstore.similarity_search(question, k=k)

        # 컨텍스트 구성
        context_parts = []
        sources = []

        for doc in results:
            doc_type = doc.metadata.get("type", "text")
            source = doc.metadata.get("source", "unknown")

            if doc_type == "image":
                context_parts.append(f"[이미지 ({source})]: {doc.page_content}")
            else:
                context_parts.append(f"[텍스트 ({source})]: {doc.page_content}")

            sources.append({
                "source": source,
                "type": doc_type,
                "content_preview": doc.page_content[:100]
            })

        context = "\n\n".join(context_parts)

        # 답변 생성
        prompt = f"""다음 정보를 바탕으로 질문에 답하세요.
이미지 설명도 포함되어 있으니 참고하세요.

정보:
{context}

질문: {question}

답변:"""

        answer = self.llm.invoke(prompt)

        return {
            "answer": answer,
            "sources": sources,
            "num_sources": len(sources)
        }

    def get_stats(self) -> Dict:
        """통계"""
        text_count = sum(1 for d in self.documents if d.metadata.get("type") == "text")
        image_count = sum(1 for d in self.documents if d.metadata.get("type") == "image")

        return {
            "total_documents": len(self.documents),
            "text_documents": text_count,
            "image_documents": image_count
        }


# 사용
rag = IntegratedMultimodalRAG()

# 텍스트 추가
rag.add_text_document(
    "LangChain은 LLM 애플리케이션 개발 프레임워크입니다.",
    "intro.md"
)

rag.add_text_document(
    "RAG는 검색 증강 생성으로, 외부 지식을 활용합니다.",
    "rag.md"
)

# 이미지 추가 (실제 이미지 필요)
# rag.add_image_document("architecture.png")

# PDF 추가 (실제 PDF 필요)
# rag.add_pdf("manual.pdf")

# 인덱스 구축
rag.build_index()

# 통계
print(rag.get_stats())

# 질문
result = rag.query("LangChain이 무엇인가요?")
print(f"답변: {result['answer']}")
print(f"출처 수: {result['num_sources']}")
