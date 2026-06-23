import streamlit as st
from src.database.auth import login_screen
from src.screens.vehicle_dashboard import vehicle_dashboard
from src.database.db import get_all_vehicles, create_vehicle, delete_vehicle
from src.ui.styles import inject_home_styles

st.set_page_config(page_title="Vehicle Management", layout="wide", page_icon="🚌")


def main():
    if not st.session_state.get("logged_in"):
        login_screen()
        return

    if "app_screen" not in st.session_state:
        st.session_state["app_screen"] = "entry"
    if "selected_vehicle" not in st.session_state:
        st.session_state["selected_vehicle"] = None

    if st.session_state["app_screen"] == "dashboard":
        vehicle_dashboard(st.session_state["selected_vehicle"])
    else:
        inject_home_styles()
        entry_screen()


def entry_screen():
    # ── Top navbar ──
    col_title, col_spacer, col_user, col_logout = st.columns([4, 2, 2, 1])
    with col_title:
        st.markdown(
            "<h2 style='font-size:1.3rem;font-weight:700;margin:0.4rem 0;color:#ffffff;'>"
            "🚌 Vehicle Management System</h2>",
            unsafe_allow_html=True,
        )
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
    with col_logout:
        if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_div, col_right = st.columns([5, 0.2, 5])

    # ── LEFT: Select existing ──
    with col_left:
        st.markdown(
            "<div class='glass-panel'><h3>📋 Select Existing Vehicle</h3>",
            unsafe_allow_html=True,
        )

        if "vehicles_list" not in st.session_state:
            st.session_state["vehicles_list"] = get_all_vehicles(
                user_id=st.session_state.get("user_id"),
                role=st.session_state.get("role"),
            )

        vehicles = st.session_state["vehicles_list"]

        if not vehicles:
            st.error("❌ No vehicles found in database.")
            st.caption("Add a new vehicle from the right panel.")
        else:
            st.success(f"✅ {len(vehicles)} vehicle(s) available")
            selected = st.selectbox(
                "Choose a vehicle",
                options=vehicles,
                format_func=lambda x: f"🚐  Bus  #{x}",
                key="vehicle_selector",
            )
            st.markdown("<br>", unsafe_allow_html=True)

            btn_col1, btn_col2 = st.columns([3, 1])
            with btn_col1:
                if st.button("➡️ Open Dashboard", key="go_dashboard", type="primary", use_container_width=True):
                    st.session_state["selected_vehicle"] = selected
                    st.session_state["app_screen"] = "dashboard"
                    st.rerun()
            with btn_col2:
                if st.button("🗑️ Delete", key="delete_vehicle_btn", use_container_width=True):
                    st.session_state["delete_confirm_vehicle"] = selected

            if st.session_state.get("delete_confirm_vehicle") == selected:
                st.warning(f"⚠️ Delete vehicle {selected} and all its related records")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Yes, Delete", key="confirm_delete", type="primary", use_container_width=True):
                        with st.spinner("Deleting..."):
                            ok = delete_vehicle(selected)
                        if ok:
                            st.success(f"✅ Bus #{selected} deleted!")
                            st.session_state.pop("delete_confirm_vehicle", None)
                            st.session_state.pop("vehicles_list", None)
                            st.rerun()
                        else:
                            st.error("❌ Delete failed. Try again.")
                with c2:
                    if st.button("❌ Cancel", key="cancel_delete", use_container_width=True):
                        st.session_state.pop("delete_confirm_vehicle", None)
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh List", key="refresh_vehicles", use_container_width=True):
            st.session_state.pop("vehicles_list", None)
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # ── DIVIDER ──
    with col_div:
        st.markdown("<div class='glass-divider'></div>", unsafe_allow_html=True)

    # ── RIGHT: Add new ──
    with col_right:
        st.markdown(
            "<div class='glass-panel'><h3>➕ Add New Vehicle</h3>",
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        new_number = st.text_input(
            "Enter Bus / Vehicle Number",
            placeholder="e.g. 0303, 3131, 7389 …",
            key="new_vehicle_input",
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚐 Create & Open", key="create_vehicle_btn", type="primary", use_container_width=True):
            raw     = new_number.strip()
            user_id = st.session_state.get("user_id")
            role    = st.session_state.get("role")

            if not raw:
                st.warning("⚠️ Vehicle number cannot be empty.")
            elif not raw.isdigit():
                st.error("❌ Only numeric values allowed (e.g. 0303, 7389).")
            else:
                current_list = get_all_vehicles(user_id=user_id, role=role)
                if raw in current_list:
                    st.warning(f"⚠️ Bus #{raw} already exists — select from left.")
                else:
                    with st.spinner(f"Creating vehicle #{raw} …"):
                        ok = create_vehicle(raw, created_by=user_id)
                    if ok:
                        st.success(f"✅ Vehicle #{raw} created!")
                        st.session_state["vehicles_list"] = get_all_vehicles(user_id=user_id, role=role)
                        st.session_state["selected_vehicle"] = raw
                        st.session_state["app_screen"] = "dashboard"
                        st.rerun()
                    else:
                        st.error("❌ Could not create vehicle. Check DB connection.")

        st.markdown("</div>", unsafe_allow_html=True)


main()