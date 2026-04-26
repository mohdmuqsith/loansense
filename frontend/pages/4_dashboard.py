import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Loan Applications Dashboard")

# Auth check
if not st.session_state.get("token"):
    st.warning("🔒 Please login first.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

# Filters
col1, col2 = st.columns([2, 1])
with col1:
    status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Approved", "Rejected", "Under Review"])
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    refresh = st.button("🔄 Refresh", use_container_width=True)

# Fetch data
try:
    params = {} if status_filter == "All" else {"status": status_filter}
    res    = requests.get(f"{API_URL}/loans/", headers=headers, params=params)

    if res.status_code == 200:
        data = res.json()

        if not data:
            st.info("No applications found.")
            st.stop()

        df = pd.DataFrame(data)

        # Stats row
        st.markdown("---")
        col3, col4, col5, col6 = st.columns(4)
        col3.metric("Total",    len(df))
        col4.metric("Approved", len(df[df["status"] == "Approved"]))
        col5.metric("Rejected", len(df[df["status"] == "Rejected"]))
        col6.metric("Pending",  len(df[df["status"] == "Pending"]))

        # Charts
        st.markdown("---")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.subheader("Applications by Status")
            status_counts = df["status"].value_counts()
            st.bar_chart(status_counts)

        with chart_col2:
            st.subheader("Applications by Area")
            if "area_type" in df.columns:
                area_counts = df["area_type"].value_counts()
                st.bar_chart(area_counts)

        # Table
        st.markdown("---")
        st.subheader("All Applications")
        display_cols = ["application_id", "full_name", "loan_amount", "loan_purpose",
                        "status", "ml_approved", "ml_confidence", "applied_at"]
        display_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(df[display_cols], use_container_width=True)

        # Review section
        st.markdown("---")
        st.subheader("Review Application")
        rcol1, rcol2, rcol3 = st.columns(3)
        with rcol1:
            review_id = st.number_input("Application ID", min_value=1, value=1)
        with rcol2:
            new_status = st.selectbox("New Status", ["Approved", "Rejected", "Under Review"])
        with rcol3:
            note = st.text_input("Note (optional)")

        if st.button("Update Status", use_container_width=True):
            update_res = requests.patch(
                f"{API_URL}/loans/{review_id}/status",
                headers=headers,
                json={"status": new_status, "note": note, "manager_id": st.session_state.manager_id}
            )
            if update_res.status_code == 200:
                st.success(f"Application {review_id} updated to {new_status}!")
                st.rerun()
            else:
                st.error(f"Error: {update_res.json().get('detail')}")

    elif res.status_code == 401:
        st.error("Session expired. Please login again.")
    else:
        st.error("Failed to load applications.")

except Exception as e:
    st.error(f"Could not connect to API: {e}")
