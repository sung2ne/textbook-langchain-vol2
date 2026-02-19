import streamlit as st
import requests
from typing import Dict, List, Optional


class RAGAPIClient:
    """RAG API 클라이언트"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def health_check(self) -> bool:
        """헬스 체크"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def query(self, question: str, k: int = 5) -> Dict:
        """질의응답"""
        response = requests.post(
            f"{self.base_url}/query",
            json={"question": question, "k": k},
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def search(self, query: str, k: int = 5) -> List[Dict]:
        """검색"""
        response = requests.post(
            f"{self.base_url}/search",
            json={"question": query, "k": k},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("results", [])

    def upload_document(self, file) -> Dict:
        """문서 업로드"""
        files = {"file": (file.name, file, file.type)}
        response = requests.post(
            f"{self.base_url}/documents/upload",
            files=files,
            timeout=60
        )
        response.raise_for_status()
        return response.json()

    def get_documents(self) -> List[str]:
        """문서 목록"""
        response = requests.get(f"{self.base_url}/documents", timeout=5)
        response.raise_for_status()
        return response.json().get("documents", [])

    def get_stats(self) -> Dict:
        """통계"""
        response = requests.get(f"{self.base_url}/stats", timeout=5)
        response.raise_for_status()
        return response.json()


# Streamlit 앱
def main():
    st.set_page_config(page_title="RAG 클라이언트", layout="wide")
    st.title("🤖 RAG 챗봇")

    # API 클라이언트 초기화
    api_url = st.sidebar.text_input("API URL", "http://localhost:8000")
    client = RAGAPIClient(api_url)

    # 연결 상태 확인
    if client.health_check():
        st.sidebar.success("✓ API 연결됨")
    else:
        st.sidebar.error("✗ API 연결 실패")
        st.error("백엔드 API에 연결할 수 없습니다.")
        return

    # 탭
    tab1, tab2, tab3 = st.tabs(["💬 채팅", "📄 문서", "📊 통계"])

    with tab1:
        render_chat(client)

    with tab2:
        render_documents(client)

    with tab3:
        render_stats(client)


def render_chat(client: RAGAPIClient):
    """채팅 인터페이스"""
    # 세션 상태
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 설정
    k = st.sidebar.slider("검색 결과 수", 1, 10, 5)

    # 대화 기록
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("sources"):
                with st.expander("출처"):
                    for src in msg["sources"]:
                        st.write(f"- {src['content'][:100]}...")

    # 입력
    if prompt := st.chat_input("질문을 입력하세요"):
        # 사용자 메시지
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # API 호출
        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):
                try:
                    result = client.query(prompt, k)
                    answer = result["answer"]
                    sources = result.get("sources", [])

                    st.write(answer)

                    if sources:
                        with st.expander("출처"):
                            for src in sources:
                                st.write(f"- {src['content'][:100]}...")

                    st.caption(f"응답 시간: {result.get('latency_ms', 0):.0f}ms")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except Exception as e:
                    st.error(f"오류: {e}")


def render_documents(client: RAGAPIClient):
    """문서 관리"""
    st.header("문서 관리")

    # 업로드
    uploaded = st.file_uploader(
        "문서 업로드",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    if uploaded and st.button("업로드"):
        for file in uploaded:
            with st.spinner(f"{file.name} 처리 중..."):
                try:
                    result = client.upload_document(file)
                    st.success(f"✓ {file.name}: {result['chunks']}개 청크")
                except Exception as e:
                    st.error(f"✗ {file.name}: {e}")

    # 문서 목록
    st.subheader("업로드된 문서")
    try:
        documents = client.get_documents()
        if documents:
            for doc in documents:
                st.write(f"📄 {doc}")
        else:
            st.info("업로드된 문서가 없습니다.")
    except Exception as e:
        st.error(f"문서 목록 조회 실패: {e}")


def render_stats(client: RAGAPIClient):
    """통계"""
    st.header("시스템 통계")

    try:
        stats = client.get_stats()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("문서 수", stats.get("document_count", 0))

        with col2:
            ready = "✓ 준비됨" if stats.get("vectorstore_ready") else "✗ 미준비"
            st.metric("벡터 스토어", ready)

    except Exception as e:
        st.error(f"통계 조회 실패: {e}")


if __name__ == "__main__":
    main()
