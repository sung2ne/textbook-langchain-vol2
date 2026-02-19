from langchain_core.documents import Document

doc = Document(
    page_content="LangChain은 LLM 프레임워크입니다.",
    metadata={
        "source": "langchain_docs.pdf",
        "page": 1,
        "author": "LangChain Team",
        "created_date": "2024-01-15",
        "category": "framework",
        "language": "ko"
    }
)
