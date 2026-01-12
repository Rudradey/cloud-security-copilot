import streamlit as st

from components.policy_upload import policy_upload_section
from components.findings_view import findings_dashboard
from components.chat_interface import ai_chat_section

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Cloud Security Copilot",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Theme State
# --------------------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# --------------------------------------------------
# Styling (Clean Dark SaaS)
# --------------------------------------------------
DARK_THEME = """
<style>
body {
    background-color: #0b0f19;
    color: #e5e7eb;
}
.card {
    background: #0f172a;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
}
.header-title {
    font-size: 30px;
    font-weight: 700;
}
.subtle {
    color: #94a3b8;
}
.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 12px;
}
</style>
"""

st.markdown(DARK_THEME, unsafe_allow_html=True)

# --------------------------------------------------
# Session State
# --------------------------------------------------
for key in ["scan_id", "scan_result", "scan_status"]:
    if key not in st.session_state:
        st.session_state[key] = None

# --------------------------------------------------
# Top Header
# --------------------------------------------------
header_left, header_right = st.columns([6, 1])

with header_left:
    st.markdown(
        "<div class='header-title'>🛡️ Cloud Security Copilot</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='subtle'>AI-powered AWS IAM risk analysis & remediation</div>",
        unsafe_allow_html=True
    )

with header_right:
    st.button("🌗 Theme", on_click=toggle_theme)

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.header("⚙️ Controls")
    hide_service_roles = st.checkbox("Hide AWS Service Roles", True)
    policy_upload_section()

# --------------------------------------------------
# Main Layout
# --------------------------------------------------
left, right = st.columns([3, 2])

# --------------------------------------------------
# Security Findings (LEFT)
# --------------------------------------------------
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔍 Security Findings</div>", unsafe_allow_html=True)
    findings_dashboard(hide_service_roles=hide_service_roles)
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# AI Advisor (RIGHT)
# --------------------------------------------------
with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🤖 AI Security Advisor</div>", unsafe_allow_html=True)
    ai_chat_section()
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.caption("FastAPI · Streamlit · AWS IAM · RAG · LLMs")
