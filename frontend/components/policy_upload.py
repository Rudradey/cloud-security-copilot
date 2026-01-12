import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"


def policy_upload_section():
    st.subheader("🚀 Scan Controls")

    if st.button("Start IAM Scan", use_container_width=True):
        try:
            response = requests.post(f"{BACKEND_URL}/scan", timeout=10)
            response.raise_for_status()

            data = response.json()
            st.session_state.scan_id = data["job_id"]
            st.session_state.scan_status = "in_progress"
            st.session_state.scan_result = None

            st.success("IAM scan started successfully")

        except Exception as exc:
            st.error(f"Failed to start scan: {exc}")

    if st.session_state.get("scan_id"):
        st.markdown(
            f"""
            <div style="margin-top:12px;padding:10px;border-radius:8px;
            background:#1e293b;color:#e5e7eb;font-size:13px;">
            <b>Scan ID</b><br>{st.session_state.scan_id}
            </div>
            """,
            unsafe_allow_html=True
        )
