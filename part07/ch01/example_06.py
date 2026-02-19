import streamlit as st
from typing import List, Dict


def display_sources(sources: List[Dict]):
    """출처 표시 컴포넌트"""
    if not sources:
        return

    st.markdown("---")
    st.markdown("**📚 출처**")

    for i, source in enumerate(sources, 1):
        with st.expander(f"출처 {i}: {source.get('title', '문서')}"):
            # 메타데이터
            col1, col2 = st.columns(2)

            with col1:
                if source.get("page"):
                    st.write(f"📄 페이지: {source['page']}")
                if source.get("source"):
                    st.write(f"📁 파일: {source['source']}")

            with col2:
                if source.get("score"):
                    st.write(f"🎯 관련도: {source['score']:.2%}")

            # 내용 미리보기
            if source.get("content"):
                st.markdown("**내용 미리보기:**")
                st.markdown(f"> {source['content'][:300]}...")


# 사용 예시
sources = [
    {
        "title": "LangChain 문서",
        "source": "langchain_guide.pdf",
        "page": 5,
        "score": 0.92,
        "content": "LangChain은 LLM 애플리케이션 개발을 위한 프레임워크입니다..."
    },
    {
        "title": "RAG 튜토리얼",
        "source": "rag_tutorial.md",
        "page": None,
        "score": 0.85,
        "content": "RAG는 Retrieval-Augmented Generation의 약자로..."
    }
]

display_sources(sources)
