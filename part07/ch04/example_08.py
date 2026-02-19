import streamlit as st
from threading import Event


class CancellableStream:
    """취소 가능한 스트리밍"""

    def __init__(self, llm):
        self.llm = llm
        self.cancel_event = Event()

    def stream(self, prompt: str):
        """취소 가능한 스트리밍"""
        self.cancel_event.clear()

        for chunk in self.llm.stream(prompt):
            if self.cancel_event.is_set():
                yield "[취소됨]"
                break
            yield chunk

    def cancel(self):
        """취소"""
        self.cancel_event.set()


# Streamlit 사용
if "streamer" not in st.session_state:
    from langchain_ollama import OllamaLLM
    st.session_state.streamer = CancellableStream(OllamaLLM(model="llama4"))

col1, col2 = st.columns([4, 1])

with col1:
    if prompt := st.chat_input("질문"):
        container = st.empty()
        full_response = ""

        for chunk in st.session_state.streamer.stream(prompt):
            full_response += chunk
            container.markdown(full_response)

with col2:
    if st.button("취소"):
        st.session_state.streamer.cancel()
