# frontend/pages/3_📊_시스템.py
import streamlit as st
from api_client import api_client


def main():
    st.title("📊 시스템")

    # 탭
    tab1, tab2, tab3 = st.tabs(["상태", "검색 테스트", "관리"])

    with tab1:
        status_section()

    with tab2:
        search_test_section()

    with tab3:
        admin_section()


def status_section():
    """상태 섹션"""
    st.subheader("시스템 상태")

    try:
        # 헬스 체크
        health = api_client.health_check()
        stats = api_client.get_stats()

        # 메트릭
        col1, col2, col3 = st.columns(3)

        with col1:
            status = "🟢 정상" if health["status"] == "healthy" else "🔴 오류"
            st.metric("상태", status)

        with col2:
            st.metric("문서 수", stats.get("document_count", 0))

        with col3:
            st.metric("청크 수", stats.get("chunk_count", 0))

        # 벡터 저장소
        st.subheader("벡터 저장소")
        col1, col2 = st.columns(2)

        with col1:
            ready = "✅ 준비됨" if health["vectorstore_ready"] else "❌ 미초기화"
            st.write(f"**상태:** {ready}")

        with col2:
            size = stats.get("vectorstore_size_mb", 0)
            st.write(f"**크기:** {size:.2f} MB")

    except Exception as e:
        st.error(f"상태 조회 실패: {e}")


def search_test_section():
    """검색 테스트 섹션"""
    st.subheader("검색 테스트")

    query = st.text_input("검색어")
    k = st.slider("결과 수", 1, 20, 10)

    if st.button("검색") and query:
        with st.spinner("검색 중..."):
            try:
                result = api_client.search(query, k)
                results = result.get("results", [])

                if not results:
                    st.info("검색 결과가 없습니다.")
                    return

                st.write(f"총 {result['total']}개 결과")

                for i, item in enumerate(results):
                    with st.expander(
                        f"[{i+1}] {item['source']} (점수: {item['score']:.3f})"
                    ):
                        st.write(item["content"])

                        if item.get("metadata"):
                            st.json(item["metadata"])

            except Exception as e:
                st.error(f"검색 실패: {e}")


def admin_section():
    """관리 섹션"""
    st.subheader("시스템 관리")

    st.warning("⚠️ 주의: 아래 작업은 되돌릴 수 없습니다.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ 벡터 저장소 초기화", type="secondary"):
            if st.session_state.get("confirm_reset"):
                try:
                    api_client.reset()
                    st.success("초기화 완료!")
                    st.session_state.confirm_reset = False
                except Exception as e:
                    st.error(f"초기화 실패: {e}")
            else:
                st.session_state.confirm_reset = True
                st.warning("다시 클릭하면 초기화됩니다.")

    with col2:
        if st.button("🔄 페이지 새로고침"):
            st.rerun()


if __name__ == "__main__":
    main()
