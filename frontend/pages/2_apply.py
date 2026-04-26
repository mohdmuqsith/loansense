import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Apply for Loan", page_icon="📝")
st.title("📝 Loan Application")

with st.form("loan_form"):
    st.subheader("Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        first_name     = st.text_input("First Name")
        age            = st.number_input("Age", min_value=18, max_value=75, value=30)
        marital_status = st.selectbox("Marital Status", ["Married", "Single", "Divorced", "Widowed"])
        education      = st.selectbox("Education Level", ["Graduate", "Not Graduate"])
    with col2:
        last_name  = st.text_input("Last Name")
        gender     = st.selectbox("Gender", ["Male", "Female", "Other"])
        dependents = st.number_input("Dependents", min_value=0, max_value=10, value=0)
        area       = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

    st.subheader("Employment")
    col3, col4 = st.columns(2)
    with col3:
        employment_status  = st.selectbox("Employment Status", ["Salaried", "Self-employed", "Contract", "Unemployed"])
        applicant_income   = st.number_input("Monthly Income", min_value=0.0, value=5000.0)
    with col4:
        employer_category  = st.selectbox("Employer Category", ["Private", "Government", "MNC", "Business", "Unemployed"])
        coapplicant_income = st.number_input("Co-applicant Income", min_value=0.0, value=0.0)

    st.subheader("Financial Profile")
    col5, col6 = st.columns(2)
    with col5:
        credit_score    = st.number_input("Credit Score", min_value=300, max_value=900, value=650)
        dti_ratio       = st.number_input("DTI Ratio", min_value=0.0, max_value=5.0, value=0.3)
        savings         = st.number_input("Savings", min_value=0.0, value=10000.0)
    with col6:
        existing_loans  = st.number_input("Existing Loans", min_value=0, max_value=10, value=0)
        collateral      = st.number_input("Collateral Value", min_value=0.0, value=0.0)

    st.subheader("Loan Details")
    col7, col8 = st.columns(2)
    with col7:
        loan_purpose = st.selectbox("Loan Purpose", ["Personal", "Car", "Home", "Business", "Education"])
        loan_amount  = st.number_input("Loan Amount", min_value=1000.0, value=50000.0)
    with col8:
        loan_term = st.selectbox("Loan Term (months)", [12, 24, 36, 48, 60, 72, 84, 120, 180, 240, 360])

    submit = st.form_submit_button("Submit Application", use_container_width=True)

if submit:
    if not first_name or not last_name:
        st.error("Please enter your full name.")
    else:
        payload = {
            "first_name": first_name, "last_name": last_name,
            "age": age, "gender": gender, "marital_status": marital_status,
            "dependents": dependents, "education_level": education,
            "area_type": area, "employer_category": employer_category,
            "employment_status": employment_status,
            "applicant_income": applicant_income,
            "coapplicant_income": coapplicant_income,
            "credit_score": credit_score, "existing_loans": existing_loans,
            "dti_ratio": dti_ratio, "savings": savings,
            "collateral_value": collateral, "loan_purpose": loan_purpose,
            "loan_amount": loan_amount, "loan_term": loan_term
        }
        try:
            res = requests.post(f"{API_URL}/loans/apply", json=payload)
            if res.status_code == 200:
                data = res.json()
                st.success("✅ Application submitted successfully!")
                st.session_state["last_application_id"] = data["application_id"]
                st.info(f"Your Application ID: **{data['application_id']}** — Go to Results page to see the decision.")
            else:
                st.error(f"Error: {res.json().get('detail', 'Something went wrong')}")
        except Exception as e:
            st.error(f"Could not connect to API: {e}")
