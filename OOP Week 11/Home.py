import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from models.security_incident import SecurityIncident

st.set_page_config(page_title="Intelligence Platform", layout="wide")

db_manager = DatabaseManager("database/platform.db")
auth_manager = AuthManager(db_manager)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = None

if not st.session_state.logged_in:
    st.title("Intelligence Platform Login")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.info("Authorized Personnel Only")
        st.markdown("Please sign in to access the secure dashboard.")

    with col2:
        tab1, tab2 = st.tabs(["🔓 Log In", "📝 Sign Up"])

        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Log In", type="primary")

                if submit:
                    user = auth_manager.login_user(username, password)
                    
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.username = user.get_username()
                        st.session_state.role = user.get_role()
                        st.rerun()
                    else:
                        st.error("Invalid credentials")

        with tab2:
            with st.form("register_form"):
                new_user = st.text_input("Choose Username")
                new_pass = st.text_input("Choose Password (min 8 chars)", type="password")
                confirm_pass = st.text_input("Confirm Password", type="password")
                submit_reg = st.form_submit_button("Create Account")

                if submit_reg:
                    if new_pass != confirm_pass:
                        st.error("Passwords do not match.")
                    elif len(new_pass) < 8:
                        st.error("Password must have at least 8 characters.")
                    else:
                        success = auth_manager.register_user(new_user, new_pass)
                        if success:
                            st.success("Account created! Please switch to the 'Log In' tab.")
                        else:
                            st.error("Username might be taken.")

else:
    st.title(f"Welcome, {st.session_state.username}")
    st.caption(f"Role: {st.session_state.role}")
    
    st.subheader("System Overview")
    
    rows = db_manager.fetch_all("SELECT id, incident_type, severity, status, description FROM security_incidents")
    incidents = [SecurityIncident(*row) for row in rows]
    
    active_count = len([i for i in incidents if i.get_status() != 'Closed'])
    resolved_count = len([i for i in incidents if i.get_status() == 'Resolved'])
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("System Status", "Online", "Stable")
    col2.metric("Active Incidents", active_count, "Critical")
    col3.metric("Resolved Incidents", resolved_count)
    
    st.divider()
    
    st.info("Navigate to Analytics for charts or Settings to manage records.")