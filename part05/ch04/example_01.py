from langchain_ollama import OllamaLLM
from langchain_core.documents import Document
from typing import List
import base64
from pathlib import Path


class ImageToTextConverter:
    """이미지를 텍스트로 변환"""

    def __init__(self, model: str = "llava"):
        self.model = model

    def describe_image(self, image_path: str) -> str:
        """이미지 설명 생성"""
        # 이미지 로드
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        # LLaVA 모델로 설명 생성
        # 실제로는 멀티모달 API 사용
        llm = OllamaLLM(model=self.model)

        prompt = """이 이미지를 상세히 설명해주세요.
        다음 내용을 포함해주세요:
        1. 이미지에 보이는 주요 요소
        2. 텍스트가 있다면 내용
        3. 다이어그램이라면 구조와 흐름
        4. 차트라면 데이터의 의미
        """

        # 실제 구현에서는 이미지와 함께 전송
        description = "이미지 설명이 생성됩니다."

        return description

    def convert_to_document(self, image_path: str) -> Document:
        """이미지를 문서로 변환"""
        description = self.describe_image(image_path)

        return Document(
            page_content=description,
            metadata={
                "source": image_path,
                "type": "image",
                "original_type": Path(image_path).suffix
            }
        )


# 사용
converter = ImageToTextConverter()
# doc = converter.convert_to_document("diagram.png")
