import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.documents import Document
from typing import List, Dict
import time


class StreamlitRAGApp:
    """Streamlit RAG 애플리케이션"""

    def __init__(self):
        self.init_session_state()

    def init_session_state(self):
        """세션 상태 초기화"""
        defaults = {
            "messages": [],
            "documents": [],
            "vectorstore": None,
            "embeddings": None,
            "llm": None,
            "settings": {
                "model": "llama4",
                "embed_model": "nomic-embed-text",
                "k": 5,
                "temperature": 0.7
            }
        }

        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    def init_models(self):
        """모델 초기화"""
        settings = st.session_state.settings

        if st.session_state.embeddings is None:
            st.session_state.embeddings = OllamaEmbeddings(
                model=settings["embed_model"]
            )

        if st.session_state.llm is None:
            st.session_state.llm = OllamaLLM(
                model=settings["model"],
                temperature=settings["temperature"]
            )

    def build_vectorstore(self, documents: List[Document]):
        """벡터 스토어 구축"""
        if not documents:
            return

        st.session_state.vectorstore = Chroma.from_documents(
            documents,
            st.session_state.embeddings
        )

    def search(self, query: str, k: int = 5) -> List[Dict]:
        """검색"""
        if st.session_state.vectorstore is None:
            return []

        results = st.session_state.vectorstore.similarity_search_with_score(
            query, k=k
        )

        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": 1 - score  # 거리를 유사도로 변환
            }
            for doc, score in results
        ]

    def generate_answer(self, query: str, contexts: List[str]) -> str:
        """답변 생성"""
        context_text = "\n\n".join(contexts)

        prompt = f"""다음 컨텍스트를 바탕으로 질문에 답하세요.
컨텍스트에 없는 정보는 "알 수 없습니다"라고 답하세요.

컨텍스트:
{context_text}

질문: {query}

답변:"""

        return st.session_state.llm.invoke(prompt)

    def render_sidebar(self):
        """사이드바 렌더링"""
        with st.sidebar:
            st.header("⚙️ 설정")

            # 모델 설정
            st.subheader("모델")
            st.session_state.settings["model"] = st.selectbox(
                "LLM 모델",
                ["llama4", "llama3.1", "mistral"]
            )

            st.session_state.settings["k"] = st.slider(
                "검색 결과 수",
                min_value=1,
                max_value=10,
                value=5
            )

            st.session_state.settings["temperature"] = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7
            )

            st.divider()

            # 통계
            st.subheader("📊 통계")
            st.write(f"문서 수: {len(st.session_state.documents)}")
            st.write(f"대화 수: {len(st.session_state.messages)}")

            st.divider()

            # 초기화 버튼
            if st.button("🗑️ 대화 초기화"):
                st.session_state.messages = []
                st.rerun()

    def render_chat(self):
        """채팅 인터페이스 렌더링"""
        # 대화 기록 표시
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

                # 출처 표시
                if msg.get("sources"):
                    with st.expander("📚 출처 보기"):
                        for source in msg["sources"]:
                            st.write(f"- {source.get('content', '')[:100]}...")

        # 입력
        if prompt := st.chat_input("질문을 입력하세요"):
            # 사용자 메시지
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })

            with st.chat_message("user"):
                st.write(prompt)

            # 검색 및 응답 생성
            with st.chat_message("assistant"):
                with st.spinner("검색 중..."):
                    results = self.search(prompt, st.session_state.settings["k"])

                if results:
                    contexts = [r["content"] for r in results]

                    with st.spinner("답변 생성 중..."):
                        answer = self.generate_answer(prompt, contexts)

                    st.write(answer)

                    # 출처 표시
                    with st.expander("📚 출처 보기"):
                        for i, result in enumerate(results, 1):
                            st.write(f"{i}. {result['content'][:100]}...")

                    # 메시지 저장
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": results
                    })
                else:
                    st.info("관련 문서를 찾을 수 없습니다. 먼저 문서를 업로드하세요.")

    def run(self):
        """앱 실행"""
        st.set_page_config(
            page_title="RAG 챗봇",
            page_icon="🤖",
            layout="wide"
        )

        st.title("🤖 RAG 챗봇")

        self.init_models()
        self.render_sidebar()

        # 메인 영역
        tab1, tab2 = st.tabs(["💬 채팅", "📄 문서 관리"])

        with tab1:
            self.render_chat()

        with tab2:
            st.header("문서 업로드")

            uploaded = st.file_uploader(
                "PDF 또는 텍스트 파일",
                type=["pdf", "txt"],
                accept_multiple_files=True
            )

            if uploaded and st.button("문서 처리"):
                with st.spinner("문서 처리 중..."):
                    all_docs = []

                    for file in uploaded:
                        chunks = process_uploaded_file(file)
                        all_docs.extend(chunks)
                        st.success(f"✓ {file.name}")

                    st.session_state.documents = all_docs
                    self.build_vectorstore(all_docs)

                    st.success(f"총 {len(all_docs)}개 청크 처리 완료!")


# 실행
if __name__ == "__main__":
    app = StreamlitRAGApp()
    app.run()
