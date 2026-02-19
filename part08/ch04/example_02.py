# frontend/streamlit_app.py
import streamlit as st


def main():
    st.set_page_config(
        page_title="Tech Docs Q&A",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📚 Tech Docs Q&A")
    st.markdown("""
    기술 문서를 업로드하고 자연어로 질문하세요.

    ### 사용 방법
    1. **문서 관리**: PDF, TXT, MD 파일 업로드
    2. **질의응답**: 문서에 대해 질문
    3. **시스템**: 상태 확인 및 관리

    👈 사이드바에서 메뉴를 선택하세요.
    """)

    # 간단한 상태 표시
    try:
        from api_client import api_client
        health = api_client.health_check()

        col1, col2 = st.columns(2)

        with col1:
            status = "🟢 정상" if health["status"] == "healthy" else "🔴 오류"
            st.metric("시스템 상태", status)

        with col2:
            st.metric("등록 문서", f"{health['document_count']}개")

    except Exception as e:
        st.error(f"❌ 백엔드 연결 실패: {e}")
        st.info("백엔드 서버가 실행 중인지 확인하세요.")


if __name__ == "__main__":
    main()
