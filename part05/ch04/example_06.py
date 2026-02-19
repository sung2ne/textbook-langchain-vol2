import fitz  # PyMuPDF
from langchain_core.documents import Document
from typing import List
from pathlib import Path


class MultimodalPDFLoader:
    """멀티모달 PDF 로더"""

    def __init__(self, image_output_dir: str = "./pdf_images"):
        self.image_output_dir = Path(image_output_dir)
        self.image_output_dir.mkdir(exist_ok=True)

    def load(self, pdf_path: str) -> List[Document]:
        """PDF 로드 (텍스트 + 이미지)"""
        documents = []

        with fitz.open(pdf_path) as doc:
            for page_num, page in enumerate(doc):
                # 텍스트 추출
                text = page.get_text()
                if text.strip():
                    documents.append(Document(
                        page_content=text,
                        metadata={
                            "source": pdf_path,
                            "page": page_num + 1,
                            "type": "text"
                        }
                    ))

                # 이미지 추출
                images = page.get_images()
                for img_idx, img in enumerate(images):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)

                    if pix.n - pix.alpha > 3:  # CMYK
                        pix = fitz.Pixmap(fitz.csRGB, pix)

                    # 이미지 저장
                    img_filename = f"{Path(pdf_path).stem}_p{page_num + 1}_img{img_idx}.png"
                    img_path = self.image_output_dir / img_filename
                    pix.save(str(img_path))

                    documents.append(Document(
                        page_content=f"[이미지: {img_filename}]",
                        metadata={
                            "source": pdf_path,
                            "page": page_num + 1,
                            "type": "image",
                            "image_path": str(img_path)
                        }
                    ))

        return documents


# 사용
# loader = MultimodalPDFLoader()
# docs = loader.load("document.pdf")
#
# for doc in docs:
#     print(f"타입: {doc.metadata['type']}, 페이지: {doc.metadata['page']}")
