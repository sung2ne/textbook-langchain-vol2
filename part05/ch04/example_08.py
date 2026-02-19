from langchain_core.documents import Document
from enum import Enum
from typing import Optional


class ImageType(Enum):
    PHOTO = "photo"
    DIAGRAM = "diagram"
    CHART = "chart"
    SCREENSHOT = "screenshot"
    TABLE = "table"
    UNKNOWN = "unknown"


class ImageTypeDetector:
    """이미지 유형 감지"""

    def detect(self, image_path: str) -> ImageType:
        """이미지 유형 감지 (실제로는 분류 모델 사용)"""
        # 파일명 기반 휴리스틱
        name = image_path.lower()

        if "diagram" in name or "flow" in name:
            return ImageType.DIAGRAM
        elif "chart" in name or "graph" in name:
            return ImageType.CHART
        elif "screenshot" in name or "screen" in name:
            return ImageType.SCREENSHOT
        elif "table" in name:
            return ImageType.TABLE
        else:
            return ImageType.PHOTO


class TypeAwareImageProcessor:
    """유형별 이미지 처리기"""

    def __init__(self):
        self.detector = ImageTypeDetector()
        self.prompts = {
            ImageType.PHOTO: "이 사진에서 보이는 내용을 설명하세요.",
            ImageType.DIAGRAM: "이 다이어그램의 구조와 흐름을 설명하세요. 각 요소간의 관계를 명확히 해주세요.",
            ImageType.CHART: "이 차트/그래프의 데이터와 의미를 설명하세요. 수치와 추세를 포함해주세요.",
            ImageType.SCREENSHOT: "이 스크린샷에서 보이는 UI 요소와 내용을 설명하세요.",
            ImageType.TABLE: "이 표의 헤더와 데이터를 텍스트로 변환해주세요.",
            ImageType.UNKNOWN: "이 이미지의 내용을 상세히 설명하세요."
        }

    def process(self, image_path: str) -> Document:
        """이미지 처리"""
        image_type = self.detector.detect(image_path)
        prompt = self.prompts[image_type]

        # 비전 모델로 설명 생성 (실제 구현)
        description = self._generate_description(image_path, prompt)

        return Document(
            page_content=description,
            metadata={
                "source": image_path,
                "type": "image",
                "image_type": image_type.value,
                "processing_prompt": prompt
            }
        )

    def _generate_description(self, image_path: str, prompt: str) -> str:
        """설명 생성 (실제로는 비전 모델 호출)"""
        return f"프롬프트 '{prompt[:30]}...'로 생성된 설명"


# 사용
processor = TypeAwareImageProcessor()

# 다이어그램 처리
# doc = processor.process("architecture_diagram.png")
# print(f"유형: {doc.metadata['image_type']}")
