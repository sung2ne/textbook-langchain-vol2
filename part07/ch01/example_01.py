import streamlit as st
from typing import List, Dict


# 세션 상태 초기화
def init_session_state():
    """세션 상태 초기화"""
    defaults = {
        "messages": [],
        "documents": [],
        "vectorstore": None,
        "settings": {
            "model": "llama4",
            "k": 5,
            "temperature": 0.7
        }
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_message(role: str, content: str, metadata: Dict = None):
    """메시지 추가"""
    message = {
        "role": role,
        "content": content,
        "metadata": metadata or {}
    }
    st.session_state.messages.append(message)


def clear_messages():
    """메시지 초기화"""
    st.session_state.messages = []


# 메인
init_session_state()

st.title("RAG 챗봇")

# 설정 사이드바
with st.sidebar:
    st.header("설정")

    st.session_state.settings["model"] = st.selectbox(
        "모델",
        ["llama4", "llama3.1", "mistral"],
        index=0
    )

    st.session_state.settings["k"] = st.slider(
        "검색 결과 수 (k)",
        min_value=1,
        max_value=10,
        value=st.session_state.settings["k"]
    )

    st.session_state.settings["temperature"] = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.settings["temperature"]
    )

    if st.button("대화 초기화"):
        clear_messages()
        st.rerun()

# 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

        # 메타데이터 표시 (출처 등)
        if msg.get("metadata", {}).get("sources"):
            with st.expander("출처 보기"):
                for source in msg["metadata"]["sources"]:
                    st.write(f"- {source}")
