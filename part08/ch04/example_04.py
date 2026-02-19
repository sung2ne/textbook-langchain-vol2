# frontend/pages/2_💬_질의응답.py
import streamlit as st
from api_client import api_client


def main():
    st.title("💬 질의응답")

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "sources" not in st.session_state:
        st.session_state.sources = []

    # 사이드바 설정
    with st.sidebar:
        st.subheader("설정")
        k = st.slider("검색 결과 수", 1, 10, 5)
        use_streaming = st.checkbox("스트리밍 모드", value=True)

        if st.button("대화 초기화"):
            st.session_state.messages = []
            st.session_state.sources = []
            st.rerun()

    # 채팅 히스토리
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 입력
    if prompt := st.chat_input("질문을 입력하세요"):
        # 사용자 메시지
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # 답변 생성
        with st.chat_message("assistant"):
            if use_streaming:
                answer = stream_response(prompt, k)
            else:
                answer = normal_response(prompt, k)

        # 답변 저장
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    # 소스 표시
    if st.session_state.sources:
        with st.expander("📚 참고 문서", expanded=False):
            for i, source in enumerate(st.session_state.sources):
                st.markdown(f"""
                **[{i+1}] {source.get('source', 'unknown')}**
                - 점수: {source.get('score', 0):.3f}

                > {source.get('content', '')[:200]}...
                """)
                st.divider()


def stream_response(question: str, k: int) -> str:
    """스트리밍 응답"""
    response_placeholder = st.empty()
    full_response = ""

    try:
        for chunk in api_client.stream_query(question, k):
            chunk_type = chunk.get("type")

            if chunk_type == "sources":
                st.session_state.sources = chunk.get("data", [])

            elif chunk_type == "token":
                full_response += chunk.get("data", "")
                response_placeholder.markdown(full_response + "▌")

            elif chunk_type == "done":
                break

            elif chunk_type == "error":
                st.error(chunk.get("data", "오류 발생"))
                return ""

        response_placeholder.markdown(full_response)
        return full_response

    except Exception as e:
        st.error(f"응답 생성 실패: {e}")
        return ""


def normal_response(question: str, k: int) -> str:
    """일반 응답"""
    with st.spinner("답변 생성 중..."):
        try:
            result = api_client.query(question, k)

            # 소스 저장
            st.session_state.sources = [
                s.dict() if hasattr(s, 'dict') else s
                for s in result.get("sources", [])
            ]

            answer = result.get("answer", "")
            st.markdown(answer)

            # 지연 시간 표시
            latency = result.get("latency_ms", 0)
            st.caption(f"⏱️ {latency:.0f}ms")

            return answer

        except Exception as e:
            st.error(f"응답 생성 실패: {e}")
            return ""


if __name__ == "__main__":
    main()
