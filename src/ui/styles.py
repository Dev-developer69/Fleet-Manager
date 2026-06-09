import streamlit as st


# ─────────────────────────────────────────────
# SHARED button/tab/alert CSS (dono screens pe)
# ─────────────────────────────────────────────
_SHARED = """
    #MainMenu, footer, header { visibility: hidden; }
    .stAppDeployButton { display: none; }

    html, body { overflow-y: auto !important; height: auto !important; }
    [data-testid="stAppViewContainer"] { overflow-y: auto !important; }
    [data-testid="stMain"] { overflow-y: auto !important; }

    .block-container {
        padding-top: 0.5rem !important;
            }

    .stButton > button[kind="primary"] {
        background: #2D6A4F !important;
        border: none !important; border-radius: 10px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(230,57,70,0.35) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        background: #48CAE4 !important;
        box-shadow: 0 6px 20px rgba(230,57,70,0.5) !important;
    }
    .stButton > button[kind="secondary"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.04) !important;
        border-radius: 10px !important; padding: 4px !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(230,57,70,0.2) !important;
        color: #e63946 !important;
    }
    .stTabs [data-baseweb="tab"] { font-weight: 600 !important; }
    .stTextInput > div > div > input { border-radius: 8px !important; }
    .stTextInput > div > div > input:focus {
        border-color: #e63946 !important;
        box-shadow: 0 0 0 2px rgba(230,57,70,0.25) !important;
    }
    .stAlert { border-radius: 10px !important; }
    hr { border-color: rgba(255,255,255,0.1) !important; }
    [data-baseweb="select"] { border-radius: 10px !important; }
    [data-testid="stDataFrame"], [data-testid="stDataEditor"] {
        border-radius: 10px !important; overflow: hidden !important;
    }
"""

# ─────────────────────────────────────────────
# HOME: background image + overlay
# ─────────────────────────────────────────────
_HOME_BG = """
    .stApp {
        background-image: url("https://raw.githubusercontent.com/Dev-developer69/vehicle-management-system/main/cv-banner.jpg") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-color: transparent !important;
        overflow-y: auto !important;
        min-height: 100vh !important;
    }
    .stApp::before {
        content: "";
        position: fixed; inset: 0;
        background: rgba(0,0,0,0.72);
        z-index: 0;
    }
    .stApp > * { position: relative; z-index: 1; }
"""

# ─────────────────────────────────────────────
# DASHBOARD: solid dark, NO image at all
# ─────────────────────────────────────────────
_DASH_BG = """
    .stApp,
    .stApp::before,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {
        background-image: none !important;
        background: #12122A !important;
    }
    .stApp::before { display: none !important; content: none !important; }
    .stApp > * { position: static !important; z-index: auto !important; }
    .stApp { overflow-y: auto !important; min-height: 100vh !important; }
"""


def inject_home_styles():
    st.markdown(f"<style>{_SHARED}{_HOME_BG}</style>", unsafe_allow_html=True)


def inject_dashboard_styles():
    st.markdown(f"<style>{_SHARED}{_DASH_BG}</style>", unsafe_allow_html=True)