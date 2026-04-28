import requests
import pandas as pd
import streamlit as st

from theme import apply_theme, render_eyebrow, render_section_header

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Audit Log", page_icon="LS", layout="wide")
apply_theme()

st.markdown(
    f"""
    <div class="hero-shell">
        {render_eyebrow("Activity trail")}
        <div class="hero-title" style="font-size: clamp(2rem, 3vw, 3rem);">Audit Log</div>
        <div class="hero-copy">
            Review who changed what, when, and why.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

if not st.session_state.get("token"):
    st.warning("Please login first.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

if st.button("Refresh"):
    st.rerun()

try:
    res = requests.get(f"{API_URL}/audit/", headers=headers)

    if res.status_code == 200:
        data = res.json()

        if not data:
            st.info("No audit records found.")
            st.stop()

        df = pd.DataFrame(data)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Changes", len(df))
        col2.metric("Approvals", len(df[df["new_status"] == "Approved"]))
        col3.metric("Rejections", len(df[df["new_status"] == "Rejected"]))

        st.markdown("---")
        st.markdown(render_section_header("Recent entries", "The most recent review actions available in the audit log."), unsafe_allow_html=True)

        display_cols = ["log_id", "application_id", "manager_name", "old_status", "new_status", "changed_at", "change_note"]
        display_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(df[display_cols], use_container_width=True)

    elif res.status_code == 401:
        st.error("Session expired. Please login again.")
    else:
        st.error("Failed to load audit log.")

except Exception as e:
    st.error(f"Could not connect to API: {e}")

