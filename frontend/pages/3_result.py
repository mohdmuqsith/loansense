import requests
import streamlit as st

from theme import apply_theme, render_eyebrow, render_section_header

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Loan Result", page_icon="LS")
apply_theme()

st.markdown(
    f"""
    <div class="hero-shell">
        {render_eyebrow("Decision output")}
        <div class="hero-title" style="font-size: clamp(2rem, 3vw, 3rem);">Loan Decision Result</div>
        <div class="hero-copy">
            Fetch the model result, confidence score, and policy explanation for a given application ID.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

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

            if data["approved"]:
                st.success("LOAN APPROVED")
            else:
                st.error("LOAN REJECTED")

            col3, col4, col5 = st.columns(3)
            col3.metric("Decision", "Approved" if data["approved"] else "Rejected")
            col4.metric("Confidence", f"{data['confidence'] * 100:.1f}%")
            col5.metric("Model", data["model_version"])

            if data.get("reasoning_text"):
                st.markdown("---")
                st.markdown(render_section_header("AI explanation", "Policy-backed reasoning attached to the prediction."), unsafe_allow_html=True)
                st.info(data["reasoning_text"])
            else:
                st.markdown("---")
                st.warning("No explanation available yet. RAG service not connected.")

        elif res.status_code == 404:
            st.warning("No prediction found for this application yet.")
        else:
            st.error(f"Error: {res.json().get('detail')}")
    except Exception as e:
        st.error(f"Could not connect to API: {e}")

