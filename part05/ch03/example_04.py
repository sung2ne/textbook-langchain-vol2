import pytesseract
from PIL import Image
from langchain_core.documents import Document


def extract_text_from_image(image_path: str, lang: str = "kor+eng") -> Document:
    """이미지에서 텍스트 추출 (OCR)"""
    image = Image.open(image_path)

    # OCR 실행
    text = pytesseract.image_to_string(image, lang=lang)

    return Document(
        page_content=text.strip(),
        metadata={
            "source": image_path,
            "type": "ocr",
            "image_size": image.size
        }
    )


# 사용
# doc = extract_text_from_image("screenshot.png")
# print(doc.page_content)
