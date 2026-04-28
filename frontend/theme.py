from html import escape
from textwrap import dedent

import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
            :root {
                --ls-bg: #f5f7fb;
                --ls-panel: #ffffff;
                --ls-panel-2: #fef8e7;
                --ls-card: #ffffff;
                --ls-border: rgba(15, 23, 42, 0.10);
                --ls-text: #0f172a;
                --ls-muted: #5b6475;
                --ls-primary: #d4a72c;
                --ls-primary-2: #f3c74d;
                --ls-accent-soft: rgba(212, 167, 44, 0.14);
                --ls-shadow: 0 18px 45px rgba(15, 23, 42, 0.10);
            }

            .stApp {
                background:
                    radial-gradient(circle at 14% 16%, rgba(212, 167, 44, 0.14), transparent 0 18%),
                    radial-gradient(circle at 86% 12%, rgba(15, 23, 42, 0.05), transparent 0 20%),
                    linear-gradient(180deg, #fbfcfe 0%, #f2f5f9 48%, #f7f9fc 100%);
                color: var(--ls-text);
                color-scheme: light;
            }

            section.main > div.block-container {
                padding-top: 2rem;
                padding-bottom: 2.5rem;
                max-width: 1240px;
            }

            h1, h2, h3, h4, h5, h6 {
                letter-spacing: -0.03em;
                color: var(--ls-text);
            }

            p, li, label, div {
                color: var(--ls-text);
            }

            [data-testid="stSidebar"] {
                background:
                    radial-gradient(circle at top, rgba(212, 167, 44, 0.10), transparent 36%),
                    linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
                border-right: 1px solid rgba(15, 23, 42, 0.08);
            }

            [data-testid="stSidebar"] * {
                color: #0f172a !important;
            }

            [data-testid="stSidebar"] .stButton button {
                background: rgba(212, 167, 44, 0.10);
                border: 1px solid rgba(212, 167, 44, 0.18);
                color: #0f172a;
            }

            .hero-shell {
                position: relative;
                overflow: hidden;
                border: 1px solid var(--ls-border);
                border-radius: 28px;
                background:
                    radial-gradient(circle at 18% 20%, rgba(212, 167, 44, 0.16), transparent 0 22%),
                    linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(247, 249, 252, 0.98));
                box-shadow: var(--ls-shadow);
                padding: 2rem;
            }

            .hero-shell::before,
            .hero-shell::after {
                content: "";
                position: absolute;
                border-radius: 999px;
                filter: blur(18px);
                pointer-events: none;
            }

            .hero-shell::before {
                width: 220px;
                height: 220px;
                right: -80px;
                top: -70px;
                background: rgba(212, 167, 44, 0.14);
            }

            .hero-shell::after {
                width: 180px;
                height: 180px;
                left: -60px;
                bottom: -70px;
                background: rgba(15, 23, 42, 0.06);
            }

            .eyebrow {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.42rem 0.8rem;
                border-radius: 999px;
                font-size: 0.84rem;
                font-weight: 700;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                background: rgba(212, 167, 44, 0.12);
                color: #7a5d00;
                border: 1px solid rgba(212, 167, 44, 0.20);
            }

            .hero-title {
                margin-top: 0.9rem;
                font-size: clamp(2.4rem, 4vw, 4.4rem);
                line-height: 1.02;
                font-weight: 800;
                color: #0f172a;
            }

            .hero-copy {
                margin-top: 1rem;
                max-width: 58ch;
                color: var(--ls-muted);
                font-size: 1.05rem;
                line-height: 1.7;
            }

            .hero-panel {
                position: relative;
                z-index: 1;
                padding: 1.4rem;
                border-radius: 22px;
                background:
                    radial-gradient(circle at top right, rgba(212, 167, 44, 0.12), transparent 0 28%),
                    linear-gradient(180deg, rgba(15, 76, 129, 0.98), rgba(13, 41, 68, 0.98));
                color: white;
                box-shadow: 0 20px 42px rgba(15, 76, 129, 0.24);
                border: 1px solid rgba(255, 255, 255, 0.08);
            }

            .hero-panel h3,
            .hero-panel p {
                color: white;
            }

            .pill-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.6rem;
                margin-top: 1.25rem;
            }

            .pill {
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                padding: 0.42rem 0.75rem;
                border-radius: 999px;
                border: 1px solid rgba(212, 167, 44, 0.20);
                background: rgba(212, 167, 44, 0.10);
                color: #7a5d00;
                font-size: 0.84rem;
                font-weight: 700;
            }

            .card-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 1rem;
                margin-top: 1rem;
            }

            .info-card {
                position: relative;
                border: 1px solid var(--ls-border);
                border-radius: 20px;
                background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(249, 251, 254, 0.98));
                box-shadow: var(--ls-shadow);
                padding: 1.15rem;
                height: 100%;
            }

            .info-card h4 {
                margin: 0;
                font-size: 1rem;
                color: #0f172a;
            }

            .info-card p {
                margin: 0.55rem 0 0;
                color: var(--ls-muted);
                line-height: 1.55;
            }

            .stat-card {
                border: 1px solid var(--ls-border);
                border-radius: 18px;
                background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(250, 252, 255, 0.98));
                box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
                padding: 1rem 1.1rem;
            }

            .stat-label {
                color: #8a6700;
                font-size: 0.84rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-weight: 700;
            }

            .stat-value {
                margin-top: 0.35rem;
                font-size: 1.6rem;
                font-weight: 800;
                color: #0f172a;
            }

            .stat-note {
                margin-top: 0.2rem;
                color: var(--ls-muted);
                font-size: 0.93rem;
            }

            .section-title {
                margin: 2rem 0 0.3rem;
                font-size: 1.45rem;
                font-weight: 800;
                color: #0f172a;
            }

            .section-subtitle {
                margin: 0;
                color: var(--ls-muted);
                line-height: 1.65;
            }

            .step-card {
                border-left: 4px solid var(--ls-primary);
                padding: 1rem 1rem 1rem 1.1rem;
                border-radius: 16px;
                background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(249, 251, 254, 0.98));
                box-shadow: 0 12px 28px rgba(15, 23, 42, 0.07);
            }

            .step-index {
                font-size: 0.8rem;
                letter-spacing: 0.08em;
                font-weight: 800;
                color: #a67c00;
                text-transform: uppercase;
            }

            .step-card h4 {
                margin: 0.45rem 0 0;
                color: #0f172a;
            }

            .step-card p {
                margin: 0.5rem 0 0;
                color: var(--ls-muted);
                line-height: 1.6;
            }

            .stButton > button {
                border-radius: 14px;
                border: 1px solid rgba(212, 167, 44, 0.24);
                background: linear-gradient(135deg, var(--ls-primary), var(--ls-primary-2));
                color: #0f172a;
                font-weight: 800;
                padding: 0.7rem 1rem;
                box-shadow: 0 12px 22px rgba(212, 167, 44, 0.16);
                transition: transform 140ms ease, box-shadow 140ms ease, opacity 140ms ease;
            }

            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 16px 28px rgba(212, 167, 44, 0.22);
            }

            .stTextInput input,
            .stNumberInput input,
            .stDateInput input,
            .stSelectbox div[data-baseweb="select"] > div,
            .stMultiSelect div[data-baseweb="select"] > div,
            textarea {
                border-radius: 14px !important;
                border: 1px solid rgba(15, 23, 42, 0.12) !important;
                background: rgba(255, 255, 255, 0.96) !important;
                color: #0f172a !important;
                box-shadow: none !important;
            }

            .stTextInput input::placeholder,
            .stNumberInput input::placeholder,
            textarea::placeholder {
                color: rgba(15, 23, 42, 0.40) !important;
            }

            .stTextInput input:focus,
            .stNumberInput input:focus,
            textarea:focus {
                border-color: rgba(212, 167, 44, 0.42) !important;
                box-shadow: 0 0 0 3px rgba(212, 167, 44, 0.08) !important;
            }

            div[data-testid="stMetric"] {
                border: 1px solid var(--ls-border);
                border-radius: 18px;
                background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(249, 251, 254, 0.98));
                padding: 1rem 1rem 0.9rem;
                box-shadow: 0 12px 26px rgba(15, 23, 42, 0.06);
            }

            div[data-testid="stDataFrame"] {
                border-radius: 18px;
                overflow: hidden;
                border: 1px solid var(--ls-border);
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
                background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(249, 251, 254, 0.98));
            }

            div[data-testid="stAlert"] {
                border-radius: 16px;
                backdrop-filter: blur(10px);
            }

            hr {
                margin: 1.5rem 0;
                border-color: rgba(15, 23, 42, 0.10);
            }

            a {
                color: #a67c00;
            }

            .stApp [data-testid="stSidebar"] .stMarkdown, 
            .stApp [data-testid="stSidebar"] p,
            .stApp [data-testid="stSidebar"] label,
            .stApp [data-testid="stSidebar"] div {
                color: #0f172a !important;
            }

            .stApp [data-testid="stSidebar"] .stToggle {
                color: #0f172a !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_eyebrow(text: str) -> str:
    return f'<div class="eyebrow">{escape(text)}</div>'


def render_section_header(title: str, subtitle: str = "") -> str:
    subtitle_html = f'<p class="section-subtitle">{escape(subtitle)}</p>' if subtitle else ""
    return f"""
        <div>
            <div class="section-title">{escape(title)}</div>
            {subtitle_html}
        </div>
    """


def stat_card(label: str, value: str, note: str = "") -> str:
    return dedent(
        f"""
        <div class="stat-card">
            <div class="stat-label">{escape(label)}</div>
            <div class="stat-value">{escape(value)}</div>
            <div class="stat-note">{escape(note)}</div>
        </div>
        """
    ).strip()


def info_card(title: str, body: str) -> str:
    return dedent(
        f"""
        <div class="info-card">
            <h4>{escape(title)}</h4>
            <p>{escape(body)}</p>
        </div>
        """
    ).strip()


def step_card(step: str, title: str, body: str) -> str:
    return dedent(
        f"""
        <div class="step-card">
            <div class="step-index">{escape(step)}</div>
            <h4>{escape(title)}</h4>
            <p>{escape(body)}</p>
        </div>
        """
    ).strip()
