import streamlit as st

from theme import apply_theme, info_card, render_eyebrow, render_section_header, stat_card, step_card

st.set_page_config(
    page_title="LoanSenseAI",
    page_icon="LS",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.manager_id = None
    st.session_state.full_name = None

st.markdown(
    f"""
    <div class="hero-shell">
        {render_eyebrow("Loan Review System")}
        <div class="hero-title">LoanSenseAI</div>
        <div class="hero-copy">
            A clean banking workflow for reviewing applications, tracking decisions, and keeping an audit trail.
            Use the pages in the sidebar to sign in, submit applications, inspect results, and review activity.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

left, right = st.columns([1.35, 1])

with left:
    st.markdown(
        render_section_header(
            "At a glance",
            "The current demo is a full-stack loan screening app with authentication, review, ML scoring, and audit history.",
        ),
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(stat_card("API", "FastAPI", "Backend on localhost:8000"), unsafe_allow_html=True)
    with c2:
        st.markdown(stat_card("UI", "Streamlit", "Fast demo-first frontend"), unsafe_allow_html=True)
    with c3:
        st.markdown(stat_card("Storage", "PostgreSQL", "Schema, seed data, audit"), unsafe_allow_html=True)

    st.write("")
    st.markdown(render_section_header("Core flow", "Everything is arranged for a quick demo and a clear review process."), unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    with g1:
        st.markdown(info_card("Manager login", "Authenticate with a seeded or newly added bank manager account."), unsafe_allow_html=True)
    with g2:
        st.markdown(info_card("Loan application", "Submit applicant details, employment, financial profile, and loan intent from one form."), unsafe_allow_html=True)
    g3, g4 = st.columns(2)
    with g3:
        st.markdown(info_card("Decision result", "View the model verdict and policy-backed explanation for each application."), unsafe_allow_html=True)
    with g4:
        st.markdown(info_card("Audit trail", "Track every manual review action with manager attribution and notes."), unsafe_allow_html=True)

with right:
    if st.session_state.token:
        status_title = "Session active"
        status_body = f"Logged in as {st.session_state.full_name}."
        status_hint = "Use the sidebar to continue into applications, results, dashboard, or audit log."
    else:
        status_title = "Ready to sign in"
        status_body = "No active session yet."
        status_hint = "Open the Login page from the sidebar to start."

    st.markdown(
        render_section_header("Session status", "A normal component card, matching the rest of the landing page."),
        unsafe_allow_html=True,
    )
    st.markdown(info_card(status_title, status_body), unsafe_allow_html=True)
    st.write("")
    st.markdown(info_card("Next step", status_hint), unsafe_allow_html=True)
    st.write("")
    st.markdown(
        """
        <div class="card-grid">
            <div class="info-card"><h4>Manager login</h4><p>Sign in from the Login page in the sidebar.</p></div>
            <div class="info-card"><h4>Application review</h4><p>Submit and inspect a loan application end to end.</p></div>
            <div class="info-card"><h4>Audit logging</h4><p>Track review actions with timestamps and notes.</p></div>
            <div class="info-card"><h4>Policy explanation</h4><p>See why a decision was approved or rejected.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown(render_section_header("Suggested demo path", "Use this flow when presenting the project."), unsafe_allow_html=True)
    st.markdown(step_card("01", "Login", "Sign in as admin or a seeded manager."), unsafe_allow_html=True)
    st.markdown(step_card("02", "Apply", "Submit a sample loan application from the application page."), unsafe_allow_html=True)
    st.markdown(step_card("03", "Inspect", "Open the result, dashboard, and audit pages to show the full workflow."), unsafe_allow_html=True)
