from langchain_core.documents import Document
from langchain_ollama import OllamaLLM
from typing import List
import base64


class VisionRAG:
    """비전 LLM 기반 RAG"""

    def __init__(self, vision_model: str = "llava", text_model: str = "llama4"):
        self.vision_model = vision_model
        self.text_model = text_model
        self.documents: List[Document] = []
        self.image_descriptions: dict = {}

    def add_document(self, doc: Document):
        """문서 추가"""
        self.documents.append(doc)

        # 이미지면 설명 생성
        if doc.metadata.get("type") == "image":
            image_path = doc.metadata.get("source")
            description = self._describe_image(image_path)
            self.image_descriptions[image_path] = description

    def _describe_image(self, image_path: str) -> str:
        """이미지 설명 생성"""
        # 실제로는 비전 모델 호출
        return f"이미지 {image_path}의 설명"

    def _load_image_base64(self, image_path: str) -> str:
        """이미지를 base64로 로드"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    def query(self, question: str, include_images: bool = True) -> str:
        """질문에 답변"""
        # 관련 문서 수집
        context_parts = []

        for doc in self.documents:
            if doc.metadata.get("type") == "image":
                image_path = doc.metadata.get("source")
                description = self.image_descriptions.get(image_path, "")
                context_parts.append(f"[이미지: {image_path}]\n{description}")
            else:
                context_parts.append(doc.page_content)

        context = "\n\n".join(context_parts)

        # LLM으로 답변 생성
        llm = OllamaLLM(model=self.text_model)

        prompt = f"""다음 정보를 바탕으로 질문에 답하세요.

정보:
{context}

질문: {question}

답변:"""

        return llm.invoke(prompt)


# 사용
rag = VisionRAG()

# 문서 추가
rag.add_document(Document(
    page_content="LangChain은 LLM 프레임워크입니다.",
    metadata={"type": "text", "source": "docs.md"}
))

# 이미지 추가
# rag.add_document(Document(
#     page_content="",
#     metadata={"type": "image", "source": "architecture.png"}
# ))

# 질문
# answer = rag.query("LangChain의 아키텍처를 설명해주세요.")
