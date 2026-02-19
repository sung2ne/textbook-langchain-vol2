import streamlit as st
from langchain_ollama import OllamaLLM
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def stream_response(prompt: str, model: str = "llama4"):
    """스트리밍 응답 생성"""
    llm = OllamaLLM(model=model)

    # 스트리밍 컨테이너
    response_container = st.empty()
    full_response = ""

    # 스트리밍 (실제로는 콜백 사용)
    for chunk in llm.stream(prompt):
        full_response += chunk
        response_container.markdown(full_response + "▌")

    response_container.markdown(full_response)

    return full_response


# 대화형 인터페이스
if prompt := st.chat_input("질문을 입력하세요"):
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.write(prompt)

    # 어시스턴트 응답 스트리밍
    with st.chat_message("assistant"):
        response = stream_response(prompt)

    # 메시지 저장
    add_message("user", prompt)
    add_message("assistant", response)
