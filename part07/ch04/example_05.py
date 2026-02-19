import streamlit as st
from langchain_ollama import OllamaLLM


def stream_with_streamlit(question: str, contexts: List[str]):
    """Streamlit에서 스트리밍"""
    # 프롬프트 구성
    context_text = "\n".join(contexts)
    prompt = f"""컨텍스트:
{context_text}

질문: {question}
답변:"""

    # 응답 컨테이너
    response_placeholder = st.empty()
    full_response = ""

    # LLM 스트리밍
    llm = OllamaLLM(model="llama4")

    for chunk in llm.stream(prompt):
        full_response += chunk
        response_placeholder.markdown(full_response + "▌")

    # 최종 응답 (커서 제거)
    response_placeholder.markdown(full_response)

    return full_response


# 사용
if prompt := st.chat_input("질문"):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # 검색 (실제로는 벡터 검색)
        contexts = ["LangChain은 LLM 프레임워크입니다."]

        response = stream_with_streamlit(prompt, contexts)
