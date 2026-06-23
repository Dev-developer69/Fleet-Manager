import streamlit as st
import hashlib
from src.database.db import get_user, create_user
from src.ui.styles import inject_home_styles


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def login_screen():
    inject_home_styles()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align:center;font-size:2.4rem;font-weight:800;'>"
        "🚌 Vehicle Management System</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:rgba(255,255,255,0.4);font-size:0.9rem;"
        "margin-bottom:2rem;'>Manage your fleet efficiently</p>",
        unsafe_allow_html=True,
    )


    st.markdown("""
        <style>
            .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    </style>
        """, unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        tab_login, tab_register = st.tabs(["🔐  Login", "📝  Register"])

        # ── LOGIN ──
        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            username = st.text_input("Username", key="login_username", placeholder="Enter username")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter password")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Login", key="login_btn", type="primary", use_container_width=True):
                if not username.strip() or not password.strip():
                    st.warning("⚠️Both username and password are required.")
                else:
                    user = get_user(username.strip())
                    if not user:
                        st.error("❌ User not found.")
                    elif user["password"] != hash_password(password):
                        st.error("❌ Wrong password.")
                    else:
                        st.session_state["logged_in"]  = True
                        st.session_state["username"]   = user["username"]
                        st.session_state["role"]       = user["role"]
                        st.session_state["user_id"]    = user["id"]
                        st.session_state["app_screen"] = "entry"
                        st.rerun()

        # ── REGISTER ──
        with tab_register:
            st.markdown("<br>", unsafe_allow_html=True)
            new_username = st.text_input("Username", key="reg_username", placeholder="Choose a username")
            new_password = st.text_input("Password", type="password", key="reg_password", placeholder="Min 4 characters")
            confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Repeat password")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Create Account", key="register_btn", type="primary", use_container_width=True):
                uname = new_username.strip()
                if not uname or not new_password:
                    st.warning("⚠️fill Sab fields.")
                elif new_password != confirm_pass:
                    st.error("❌ Passwords does not match")
                elif len(new_password) < 4:
                    st.warning("⚠️Minimum 4 characters required for Password.")
                else:
                    existing = get_user(uname)
                    if existing:
                        st.error("❌ Username already taken.")
                    else:
                        ok = create_user(uname, hash_password(new_password), role="user")
                        if ok:
                            st.success("✅ Account created! Now login")
                        else:
                            st.error("❌ Registration failed. Try again.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align:center;color:rgba(255,255,255,0.15);font-size:0.75rem;'>"
            "© 2025 Vehicle Management System</p>",
            unsafe_allow_html=True,
        )