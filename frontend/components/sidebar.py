import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/bank.png", width=60)
        st.title("LoanSenseAI")
        st.markdown("---")

        if st.session_state.get("token"):
            st.success(f"👤 {st.session_state.full_name}")
            if st.button("Logout", use_container_width=True):
                st.session_state.token      = None
                st.session_state.manager_id = None
                st.session_state.full_name  = None
                st.rerun()
        else:
            st.warning("Not logged in")
