import streamlit as st
import time


def typing_effect(text: str, delay: float = 0.02):
    """타이핑 효과"""
    container = st.empty()
    displayed = ""

    for char in text:
        displayed += char
        container.markdown(displayed + "▌")
        time.sleep(delay)

    container.markdown(displayed)


def stream_with_typing(llm, prompt: str, min_delay: float = 0.01,
                      max_delay: float = 0.05):
    """자연스러운 스트리밍"""
    import random

    container = st.empty()
    full_response = ""

    for chunk in llm.stream(prompt):
        full_response += chunk
        container.markdown(full_response + "▌")

        # 문장 부호 후 더 긴 지연
        if chunk in ".!?":
            time.sleep(max_delay * 3)
        elif chunk in ",;:":
            time.sleep(max_delay * 2)
        else:
            time.sleep(random.uniform(min_delay, max_delay))

    container.markdown(full_response)
    return full_response
