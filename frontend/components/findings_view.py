import streamlit as st
import requests
import time
from collections import defaultdict

BACKEND_URL = "http://localhost:8000"
POLL_INTERVAL = 3


def findings_dashboard(hide_service_roles: bool = True):
    if not st.session_state.get("scan_id"):
        st.info("Start a scan to view findings")
        return

    try:
        response = requests.get(
            f"{BACKEND_URL}/scan/{st.session_state.scan_id}",
            timeout=10
        )
        response.raise_for_status()
    except Exception as exc:
        st.error(f"Failed to fetch scan status: {exc}")
        return

    job = response.json()
    st.session_state.scan_status = job["status"]

    st.markdown(f"**Status:** `{job['status']}`")

    if job["status"] == "in_progress":
        time.sleep(POLL_INTERVAL)
        st.rerun()

    if job["status"] == "failed":
        st.error("Scan failed")
        st.write(job.get("error", "Unknown error"))
        return

    if job["status"] != "completed":
        return

    st.success("Scan completed")
    st.session_state.scan_result = job["data"]

    severity_count = defaultdict(int)

    for role in st.session_state.scan_result.get("roles", []):
        role_name = role["RoleName"]

        if hide_service_roles and role_name.startswith("AWSServiceRole"):
            continue

        with st.expander(f"👤 Role: {role_name}", expanded=False):
            for policy in role.get("AttachedPolicies", []):
                st.markdown(f"**Policy:** `{policy['PolicyName']}`")
                st.markdown(f"**Risk Score:** `{policy['RiskScore']}`")

                seen = set()
                for finding in policy.get("Findings", []):
                    key = (finding["title"], finding["severity"])
                    if key in seen:
                        continue
                    seen.add(key)

                    severity_count[finding["severity"]] += 1

                    st.markdown(
                        f"- **{finding['title']}** "
                        f"(`{finding['severity']}`)"
                    )

    st.divider()
    st.subheader("📊 Severity Summary")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CRITICAL", severity_count.get("CRITICAL", 0))
    c2.metric("HIGH", severity_count.get("HIGH", 0))
    c3.metric("MEDIUM", severity_count.get("MEDIUM", 0))
    c4.metric("LOW", severity_count.get("LOW", 0))
