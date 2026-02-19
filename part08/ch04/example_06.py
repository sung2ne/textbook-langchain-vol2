# frontend/components/chat.py
import streamlit as st
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Message:
    """채팅 메시지"""
    role: str  # "user" or "assistant"
    content: str
    sources: Optional[List[dict]] = None


class ChatComponent:
    """채팅 컴포넌트"""

    def __init__(self, key: str = "chat"):
        self.key = key

        if f"{key}_messages" not in st.session_state:
            st.session_state[f"{key}_messages"] = []

    @property
    def messages(self) -> List[Message]:
        return st.session_state[f"{self.key}_messages"]

    def add_message(self, role: str, content: str,
                   sources: List[dict] = None):
        """메시지 추가"""
        msg = Message(role=role, content=content, sources=sources)
        st.session_state[f"{self.key}_messages"].append(msg)

    def clear(self):
        """채팅 초기화"""
        st.session_state[f"{self.key}_messages"] = []

    def render(self):
        """채팅 렌더링"""
        for msg in self.messages:
            with st.chat_message(msg.role):
                st.markdown(msg.content)

                if msg.sources:
                    with st.expander("📚 참고 문서"):
                        for i, src in enumerate(msg.sources):
                            st.markdown(f"""
                            **[{i+1}] {src.get('source', '')}**
                            > {src.get('content', '')[:150]}...
                            """)


class StreamingChat:
    """스트리밍 채팅"""

    def __init__(self, api_client, k: int = 5):
        self.api_client = api_client
        self.k = k
        self.chat = ChatComponent()

    def send(self, question: str) -> str:
        """메시지 전송"""
        # 사용자 메시지
        self.chat.add_message("user", question)

        # 응답 생성
        response_placeholder = st.empty()
        full_response = ""
        sources = []

        try:
            for chunk in self.api_client.stream_query(question, self.k):
                if chunk["type"] == "sources":
                    sources = chunk["data"]

                elif chunk["type"] == "token":
                    full_response += chunk["data"]
                    response_placeholder.markdown(full_response + "▌")

                elif chunk["type"] == "done":
                    break

            response_placeholder.markdown(full_response)

            # 어시스턴트 메시지
            self.chat.add_message("assistant", full_response, sources)

            return full_response

        except Exception as e:
            st.error(f"오류: {e}")
            return ""
