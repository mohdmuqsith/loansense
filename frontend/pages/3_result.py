import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Loan Result", page_icon="🤖")
st.title("🤖 Loan Decision Result")

app_id = st.session_state.get("last_application_id", None)

col1, col2 = st.columns([2, 1])
with col1:
    app_id_input = st.number_input("Application ID", min_value=1, value=int(app_id) if app_id else 1)
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    check = st.button("Get Result", use_container_width=True)

if check:
    try:
        res = requests.get(f"{API_URL}/predictions/{app_id_input}")
        if res.status_code == 200:
            data = res.json()

            # Decision banner
            if data["approved"]:
                st.success("## ✅ LOAN APPROVED")
            else:
                st.error("## ❌ LOAN REJECTED")

            # Metrics
            col3, col4, col5 = st.columns(3)
            col3.metric("Decision", "Approved ✅" if data["approved"] else "Rejected ❌")
            col4.metric("Confidence", f"{data['confidence'] * 100:.1f}%")
            col5.metric("Model", data["model_version"])

            # RAG Explanation
            if data.get("reasoning_text"):
                st.markdown("---")
                st.subheader("📋 AI Explanation")
                st.info(data["reasoning_text"])
            else:
                st.markdown("---")
                st.warning("No explanation available yet — RAG service not connected.")

        elif res.status_code == 404:
            st.warning("No prediction found for this application yet.")
        else:
            st.error(f"Error: {res.json().get('detail')}")
    except Exception as e:
        st.error(f"Could not connect to API: {e}")
