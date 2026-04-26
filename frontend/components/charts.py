import streamlit as st
import pandas as pd


def approval_pie_chart(df: pd.DataFrame):
    status_counts = df["status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    st.bar_chart(status_counts.set_index("Status"))


def credit_score_chart(df: pd.DataFrame):
    if "credit_score" in df.columns:
        st.subheader("Credit Score Distribution")
        st.bar_chart(df["credit_score"].value_counts().sort_index())


def loan_amount_chart(df: pd.DataFrame):
    if "loan_amount" in df.columns:
        st.subheader("Loan Amount Distribution")
        st.bar_chart(df["loan_amount"])
