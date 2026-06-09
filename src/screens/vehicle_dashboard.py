import streamlit as st
from src.ui.excel_format import editable_grid, driver_salary, expenses, salary_check_view
from src.ui.styles import inject_dashboard_styles


def vehicle_dashboard(bus_number: str):
    inject_dashboard_styles() 

    # ── Top bar ──
    col_title, col_spacer, col_user, col_back = st.columns([4, 2, 2, 1])
    with col_title:
        st.markdown(f"### 🚐 Bus #{bus_number} — Dashboard",)
    with col_user:
        role  = st.session_state.get("role", "user")
        uname = st.session_state.get("username", "")
        badge_color = "#e63946" if role == "admin" else "#4cc9f0"
        badge_icon  = "🛡️" if role == "admin" else "👤"
        st.markdown(
            f"<div style='text-align:right;padding-top:0.6rem;'>"
            f"<span style='background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);"
            f"border-radius:20px;padding:4px 14px;font-size:0.85rem;color:{badge_color};font-weight:600;'>"
            f"{badge_icon} {uname} ({role})</span></div>",
            unsafe_allow_html=True,
        )
    with col_back:
        st.markdown("<div style='padding-top:0.4rem;'>", unsafe_allow_html=True)
        if st.button("⬅️ Back", key="back_btn", use_container_width=True):
            keys_to_drop = [k for k in list(st.session_state.keys()) if str(bus_number) in k]
            for k in keys_to_drop:
                del st.session_state[k]
            st.session_state["selected_vehicle"] = None
            st.session_state["app_screen"] = "entry"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Vehicle Records",
        "💰 Driver Salary",
        "🧾 Expenses",
        "📊 Salary Check",
    ])

    with tab1:
        editable_grid(bus_number)
    with tab2:
        driver_salary(bus_number)
    with tab3:
        expenses(bus_number)
    with tab4:
        salary_check_view()