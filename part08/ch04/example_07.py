# frontend/components/document.py
import streamlit as st
from typing import List, Callable
from dataclasses import dataclass


@dataclass
class DocumentInfo:
    """문서 정보"""
    id: str
    filename: str
    chunks: int
    size_bytes: int


class DocumentUploader:
    """문서 업로더 컴포넌트"""

    def __init__(self, api_client, on_upload: Callable = None):
        self.api_client = api_client
        self.on_upload = on_upload

    def render(self):
        """렌더링"""
        files = st.file_uploader(
            "파일 선택",
            type=["pdf", "txt", "md", "docx"],
            accept_multiple_files=True
        )

        if files and st.button("업로드", type="primary"):
            self._upload_files(files)

    def _upload_files(self, files):
        """파일 업로드"""
        progress = st.progress(0)
        results = []

        for i, file in enumerate(files):
            try:
                result = self.api_client.upload_document(file)
                results.append({
                    "file": file.name,
                    "success": result.get("status") == "success",
                    "chunks": result.get("chunks", 0)
                })
            except Exception as e:
                results.append({
                    "file": file.name,
                    "success": False,
                    "error": str(e)
                })

            progress.progress((i + 1) / len(files))

        # 결과 표시
        for r in results:
            if r["success"]:
                st.success(f"✅ {r['file']}: {r['chunks']}개 청크")
            else:
                st.error(f"❌ {r['file']}: {r.get('error', '실패')}")

        if self.on_upload:
            self.on_upload(results)


class DocumentList:
    """문서 목록 컴포넌트"""

    def __init__(self, api_client, on_delete: Callable = None):
        self.api_client = api_client
        self.on_delete = on_delete

    def render(self):
        """렌더링"""
        try:
            result = self.api_client.list_documents()
            documents = result.get("documents", [])

            if not documents:
                st.info("등록된 문서가 없습니다.")
                return

            st.write(f"총 {len(documents)}개 문서")

            for doc in documents:
                self._render_document(doc)

        except Exception as e:
            st.error(f"목록 조회 실패: {e}")

    def _render_document(self, doc: dict):
        """문서 렌더링"""
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

            with col1:
                st.write(f"📄 **{doc['filename']}**")

            with col2:
                st.write(f"{doc['chunks']} 청크")

            with col3:
                size_kb = doc['size_bytes'] / 1024
                st.write(f"{size_kb:.1f} KB")

            with col4:
                if st.button("🗑️", key=f"del_{doc['id']}"):
                    self._delete_document(doc['id'])

            st.divider()

    def _delete_document(self, doc_id: str):
        """문서 삭제"""
        try:
            self.api_client.delete_document(doc_id)
            st.success("삭제 완료!")

            if self.on_delete:
                self.on_delete(doc_id)

            st.rerun()

        except Exception as e:
            st.error(f"삭제 실패: {e}")
