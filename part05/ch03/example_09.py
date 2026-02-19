from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from typing import List
import pdfplumber
import re


class CompletePDFProcessor:
    """PDF 완전 처리기"""

    def __init__(self):
        self.table_pattern = re.compile(r'\|.+\|')

    def process(self, pdf_path: str) -> dict:
        """PDF 완전 처리"""
        result = {
            "text_documents": [],
            "table_documents": [],
            "metadata": {"source": pdf_path}
        }

        # 텍스트 추출
        loader = PyPDFLoader(pdf_path)
        text_docs = loader.load()
        result["text_documents"] = text_docs

        # 표 추출
        table_docs = self._extract_tables(pdf_path)
        result["table_documents"] = table_docs

        return result

    def _extract_tables(self, pdf_path: str) -> List[Document]:
        """표 추출"""
        documents = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()

                    for table_num, table in enumerate(tables):
                        if not table or len(table) < 2:
                            continue

                        # 자연어로 변환
                        natural_text = self._table_to_text(table)

                        doc = Document(
                            page_content=natural_text,
                            metadata={
                                "source": pdf_path,
                                "page": page_num + 1,
                                "table_index": table_num,
                                "type": "table"
                            }
                        )
                        documents.append(doc)

        except Exception as e:
            print(f"표 추출 오류: {e}")

        return documents

    def _table_to_text(self, table: List[List]) -> str:
        """표를 텍스트로 변환"""
        if not table or not table[0]:
            return ""

        headers = [str(h or "").strip() for h in table[0]]
        rows = table[1:]

        text_parts = []
        for row in rows:
            cells = [str(c or "").strip() for c in row]
            if len(cells) >= len(headers):
                row_desc = ", ".join(f"{headers[i]}: {cells[i]}"
                                     for i in range(len(headers)))
                text_parts.append(row_desc)

        return "\n".join(text_parts)

    def get_all_documents(self, pdf_path: str) -> List[Document]:
        """모든 문서 반환"""
        result = self.process(pdf_path)
        return result["text_documents"] + result["table_documents"]


# 사용 예시
# processor = CompletePDFProcessor()
# all_docs = processor.get_all_documents("document.pdf")
#
# print(f"텍스트: {len([d for d in all_docs if d.metadata.get('type') != 'table'])}개")
# print(f"표: {len([d for d in all_docs if d.metadata.get('type') == 'table'])}개")
