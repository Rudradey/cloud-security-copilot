import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"


def ai_chat_section():
    if st.session_state.get("scan_status") != "completed":
        st.info("Complete a scan to enable AI explanations")
        return

    if st.button("🧠 Explain Findings", use_container_width=True):
        with st.spinner("AI analyzing security risks..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/explain",
                    json={"scan_id": st.session_state.scan_id},
                    timeout=60
                )
                response.raise_for_status()

                results = response.json().get("results", [])

                if not results:
                    st.info("No findings to explain")
                    return

                for item in results:
                    with st.expander(
                        f"📄 {item['Role']} → {item['Policy']}",
                        expanded=False
                    ):
                        explanation = item["Explanation"]

                        st.markdown(explanation["summary"])

                        for detail in explanation["details"]:
                            st.markdown(
                                f"**{detail['severity']}** — {detail['explanation']}"
                            )

                        st.markdown("**🔐 Secure Policy Template:**")
                        st.json(explanation["recommended_policy"])

            except Exception as exc:
                st.error(f"AI explanation failed: {exc}")
