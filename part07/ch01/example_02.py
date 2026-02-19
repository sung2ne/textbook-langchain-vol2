import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import os


def process_uploaded_file(uploaded_file) -> List:
    """업로드된 파일 처리"""
    # 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        # 파일 유형별 로더
        if uploaded_file.name.endswith(".pdf"):
            loader = PyPDFLoader(tmp_path)
        elif uploaded_file.name.endswith(".txt"):
            loader = TextLoader(tmp_path, encoding="utf-8")
        else:
            st.error(f"지원하지 않는 파일 형식: {uploaded_file.name}")
            return []

        documents = loader.load()

        # 분할
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)

        return chunks

    finally:
        # 임시 파일 삭제
        os.unlink(tmp_path)


# UI
st.header("문서 업로드")

uploaded_files = st.file_uploader(
    "PDF 또는 텍스트 파일 업로드",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("문서 처리 중..."):
        all_chunks = []

        for file in uploaded_files:
            chunks = process_uploaded_file(file)
            all_chunks.extend(chunks)
            st.success(f"✓ {file.name}: {len(chunks)}개 청크")

        st.session_state.documents = all_chunks
        st.info(f"총 {len(all_chunks)}개 청크 처리됨")
