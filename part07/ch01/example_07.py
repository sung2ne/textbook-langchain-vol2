import streamlit as st
from typing import List, Dict


def display_search_results(query: str, results: List[Dict]):
    """검색 결과 시각화"""
    st.subheader(f"🔍 '{query}' 검색 결과")

    if not results:
        st.info("검색 결과가 없습니다.")
        return

    # 결과 요약
    st.write(f"총 {len(results)}개 결과")

    # 결과 목록
    for i, result in enumerate(results, 1):
        score = result.get("score", 0)

        # 점수에 따른 색상
        if score >= 0.8:
            color = "🟢"
        elif score >= 0.6:
            color = "🟡"
        else:
            color = "🔴"

        with st.container():
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"**{i}. {result.get('title', '문서')}** {color}")
                st.markdown(f"_{result.get('content', '')[:150]}..._")

            with col2:
                st.metric("관련도", f"{score:.0%}")

            st.divider()


# 테스트
test_results = [
    {"title": "LangChain 소개", "content": "LangChain은 LLM 프레임워크...", "score": 0.95},
    {"title": "RAG 개념", "content": "RAG는 검색 증강 생성...", "score": 0.82},
    {"title": "벡터 DB", "content": "벡터 데이터베이스는...", "score": 0.65},
]

display_search_results("LangChain", test_results)
