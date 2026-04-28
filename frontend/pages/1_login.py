import requests
import streamlit as st

from theme import apply_theme, render_eyebrow, render_section_header

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Login", page_icon="LS")
apply_theme()

st.markdown(
    f"""
    <div class="hero-shell">
        {render_eyebrow("Secure access")}
        <div class="hero-title" style="font-size: clamp(2rem, 3vw, 3rem);">Bank Manager Login</div>
        <div class="hero-copy">
            Sign in to review applications, make decisions, and keep the audit trail consistent.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

if st.session_state.get("token"):
    st.success(f"Already logged in as {st.session_state.full_name}.")
    if st.button("Logout", use_container_width=True):
        st.session_state.token = None
        st.session_state.manager_id = None
        st.session_state.full_name = None
        st.rerun()
else:
    left, right = st.columns([1.1, 0.9])

    with left:
        st.markdown(render_section_header("Enter credentials", "Use your seeded manager account or a newly added one."), unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="manager1")
            password = st.text_input("Password", type="password", placeholder="password123")
            submit = st.form_submit_button("Login", use_container_width=True)

        if submit:
            if not username or not password:
                st.error("Please enter username and password.")
            else:
                try:
                    res = requests.post(
                        f"{API_URL}/auth/login",
                        data={"username": username, "password": password},
                    )
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.token = data["access_token"]
                        st.session_state.manager_id = data["manager_id"]
                        st.session_state.full_name = data["full_name"]
                        st.success(f"Welcome, {data['full_name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                except Exception as e:
                    st.error(f"Could not connect to API: {e}")

    with right:
        st.markdown(
            """
            <div class="info-card">
                <h4>Demo accounts</h4>
                <p><strong>admin</strong> / password123</p>
                <p><strong>manager1</strong> / password123</p>
                <p><strong>manager2</strong> / password123</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown(
            """
            <div class="info-card">
                <h4>What happens after login</h4>
                <p>You can review applications, check model decisions, and inspect the audit log from the sidebar pages.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

