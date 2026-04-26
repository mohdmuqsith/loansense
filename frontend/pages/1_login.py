import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Login", page_icon="🔒")
st.title("🔒 Bank Manager Login")

if st.session_state.get("token"):
    st.success(f"Already logged in as **{st.session_state.full_name}**")
    if st.button("Logout"):
        st.session_state.token      = None
        st.session_state.manager_id = None
        st.session_state.full_name  = None
        st.rerun()
else:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit   = st.form_submit_button("Login")

    if submit:
        if not username or not password:
            st.error("Please enter username and password.")
        else:
            try:
                res = requests.post(f"{API_URL}/auth/login", data={
                    "username": username,
                    "password": password
                })
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.token      = data["access_token"]
                    st.session_state.manager_id = data["manager_id"]
                    st.session_state.full_name  = data["full_name"]
                    st.success(f"Welcome, {data['full_name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            except Exception as e:
                st.error(f"Could not connect to API: {e}")
