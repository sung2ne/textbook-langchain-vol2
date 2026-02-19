import streamlit as st
import time


def process_with_progress(items: list, process_func, description: str = "처리 중"):
    """진행 상황과 함께 처리"""
    results = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, item in enumerate(items):
        # 진행률 업데이트
        progress = (i + 1) / len(items)
        progress_bar.progress(progress)
        status_text.text(f"{description}... {i + 1}/{len(items)}")

        # 처리
        result = process_func(item)
        results.append(result)

    progress_bar.empty()
    status_text.empty()

    return results


# 사용 예시
def dummy_process(item):
    time.sleep(0.1)
    return item.upper()

items = ["item1", "item2", "item3", "item4", "item5"]

if st.button("처리 시작"):
    results = process_with_progress(items, dummy_process, "항목 처리")
    st.write(f"결과: {results}")
