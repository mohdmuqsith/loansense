import streamlit as st

st.set_page_config(
    page_title="LoanSenseAI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Redirect to login if not authenticated
if "token" not in st.session_state:
    st.session_state.token      = None
    st.session_state.manager_id = None
    st.session_state.full_name  = None

st.title("🏦 LoanSenseAI")
st.markdown("### AI-Powered Loan Approval System")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.info("👈 Use the sidebar to navigate")

with col2:
    if st.session_state.token:
        st.success(f"✅ Logged in as **{st.session_state.full_name}**")
    else:
        st.warning("🔒 Please login to access the dashboard")
