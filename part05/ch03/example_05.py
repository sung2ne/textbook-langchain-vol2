from pdf2image import convert_from_path
import pytesseract


def pdf_to_text_via_ocr(pdf_path: str) -> List[Document]:
    """PDF를 이미지로 변환 후 OCR"""
    documents = []

    # PDF를 이미지로 변환
    images = convert_from_path(pdf_path)

    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang="kor+eng")

        if text.strip():
            doc = Document(
                page_content=text.strip(),
                metadata={
                    "source": pdf_path,
                    "page": i + 1,
                    "type": "ocr"
                }
            )
            documents.append(doc)

    return documents


# 스캔 PDF에 유용
# docs = pdf_to_text_via_ocr("scanned_document.pdf")
