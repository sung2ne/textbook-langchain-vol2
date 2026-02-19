# frontend/pages/1_📄_문서관리.py
import streamlit as st
from api_client import api_client


def main():
    st.title("📄 문서 관리")

    # 탭
    tab1, tab2 = st.tabs(["업로드", "문서 목록"])

    with tab1:
        upload_section()

    with tab2:
        document_list_section()


def upload_section():
    """업로드 섹션"""
    st.subheader("문서 업로드")

    uploaded_files = st.file_uploader(
        "파일 선택",
        type=["pdf", "txt", "md", "docx"],
        accept_multiple_files=True,
        help="PDF, TXT, MD, DOCX 파일을 업로드하세요."
    )

    if uploaded_files:
        if st.button("업로드", type="primary"):
            progress = st.progress(0)
            status = st.empty()

            for i, file in enumerate(uploaded_files):
                status.text(f"업로드 중: {file.name}")

                try:
                    result = api_client.upload_document(file)

                    if result.get("status") == "success":
                        st.success(f"✅ {file.name}: {result['chunks']}개 청크")
                    else:
                        st.error(f"❌ {file.name}: 업로드 실패")

                except Exception as e:
                    st.error(f"❌ {file.name}: {e}")

                progress.progress((i + 1) / len(uploaded_files))

            status.text("완료!")
            st.balloons()


def document_list_section():
    """문서 목록 섹션"""
    st.subheader("등록된 문서")

    try:
        result = api_client.list_documents()
        documents = result.get("documents", [])

        if not documents:
            st.info("등록된 문서가 없습니다.")
            return

        st.write(f"총 {result['total']}개 문서")

        for doc in documents:
            with st.expander(f"📄 {doc['filename']}"):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(f"**ID:** {doc['id']}")

                with col2:
                    st.write(f"**청크:** {doc['chunks']}개")

                with col3:
                    size_kb = doc['size_bytes'] / 1024
                    st.write(f"**크기:** {size_kb:.1f} KB")

                # 삭제 버튼
                if st.button(f"삭제", key=f"del_{doc['id']}"):
                    try:
                        api_client.delete_document(doc['id'])
                        st.success("삭제 완료!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"삭제 실패: {e}")

    except Exception as e:
        st.error(f"문서 목록 조회 실패: {e}")


if __name__ == "__main__":
    main()
