import streamlit as st


# 탭 레이아웃
tab1, tab2, tab3 = st.tabs(["💬 채팅", "📄 문서", "⚙️ 설정"])

with tab1:
    st.header("채팅")
    # 채팅 인터페이스

with tab2:
    st.header("문서 관리")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("업로드된 문서")
        for i, doc in enumerate(st.session_state.get("documents", [])):
            with st.expander(f"문서 {i + 1}"):
                st.write(doc.page_content[:200] + "...")
                st.json(doc.metadata)

    with col2:
        st.subheader("통계")
        st.metric("총 문서 수", len(st.session_state.get("documents", [])))
        st.metric("총 문자 수", sum(
            len(d.page_content) for d in st.session_state.get("documents", [])
        ))

with tab3:
    st.header("설정")
    # 설정 UI
