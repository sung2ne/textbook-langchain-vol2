from langchain_ollama import OllamaLLM
from langchain_core.documents import Document
import base64


def generate_image_caption(image_path: str) -> Document:
    """이미지 캡션 생성 (비전 모델)"""
    # 이미지를 base64로 인코딩
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    # LLaVA 등 비전 모델 사용
    llm = OllamaLLM(model="llava")

    prompt = f"""다음 이미지를 설명해주세요.
    이미지에서 볼 수 있는 내용, 텍스트, 다이어그램 등을 상세히 설명하세요.

    [이미지: data:image/png;base64,{image_data[:100]}...]
    """

    # 실제로는 멀티모달 API 사용 필요
    caption = "이미지 설명이 여기에 생성됩니다."

    return Document(
        page_content=caption,
        metadata={
            "source": image_path,
            "type": "image_caption"
        }
    )
