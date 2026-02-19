import pdfplumber
from langchain_core.documents import Document


def extract_tables_from_pdf(pdf_path: str) -> List[Document]:
    """PDF에서 표 추출"""
    documents = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()

            for table_num, table in enumerate(tables):
                if not table or not table[0]:
                    continue

                # 헤더와 데이터 분리
                headers = table[0]
                data_rows = table[1:]

                # 마크다운 형식으로 변환
                md_lines = []
                md_lines.append("| " + " | ".join(str(h or "") for h in headers) + " |")
                md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

                for row in data_rows:
                    md_lines.append("| " + " | ".join(str(c or "") for c in row) + " |")

                md_table = "\n".join(md_lines)

                doc = Document(
                    page_content=md_table,
                    metadata={
                        "source": pdf_path,
                        "page": page_num + 1,
                        "table_index": table_num,
                        "type": "table"
                    }
                )
                documents.append(doc)

    return documents


# 사용
# table_docs = extract_tables_from_pdf("document.pdf")
