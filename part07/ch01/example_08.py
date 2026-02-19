import streamlit as st
import time
from datetime import datetime


def create_monitoring_dashboard():
    """모니터링 대시보드"""
    st.header("📊 시스템 모니터링")

    # 메트릭 행
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "총 질문 수",
            len(st.session_state.get("messages", [])) // 2,
            delta=1
        )

    with col2:
        st.metric(
            "문서 수",
            len(st.session_state.get("documents", [])),
            delta=None
        )

    with col3:
        avg_latency = st.session_state.get("avg_latency", 0)
        st.metric(
            "평균 응답 시간",
            f"{avg_latency:.1f}s",
            delta=f"-{0.1:.1f}s" if avg_latency > 0 else None
        )

    with col4:
        st.metric(
            "상태",
            "정상 ✓",
            delta=None
        )

    # 최근 활동
    st.subheader("최근 활동")

    activities = st.session_state.get("activities", [])
    if activities:
        for activity in activities[-5:]:
            st.write(f"• {activity['time']} - {activity['action']}")
    else:
        st.info("아직 활동이 없습니다.")


def log_activity(action: str):
    """활동 로깅"""
    if "activities" not in st.session_state:
        st.session_state.activities = []

    st.session_state.activities.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "action": action
    })


# 사용
create_monitoring_dashboard()
