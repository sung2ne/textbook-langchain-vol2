import streamlit as st
import requests
import json


def stream_from_api(question: str, api_url: str):
    """API에서 스트리밍으로 응답 받기"""
    response = requests.get(
        f"{api_url}/stream",
        params={"question": question},
        stream=True
    )

    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8")
            if line.startswith("data: "):
                data = json.loads(line[6:])
                yield data


def render_streaming_chat(api_url: str):
    """스트리밍 채팅"""
    if prompt := st.chat_input("질문"):
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            response_container = st.empty()
            sources_container = st.empty()

            full_response = ""
            sources = []

            for data in stream_from_api(prompt, api_url):
                if data["type"] == "sources":
                    sources = data["content"]

                elif data["type"] == "token":
                    full_response += data["content"]
                    response_container.markdown(full_response + "▌")

                elif data["type"] == "done":
                    response_container.markdown(full_response)

            # 출처 표시
            if sources:
                with sources_container.expander("출처"):
                    for src in sources:
                        st.write(f"- {src['content'][:100]}...")
