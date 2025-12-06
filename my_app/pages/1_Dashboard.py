import streamlit as st
from incidents import get_all_incidents 

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must login to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.set_page_config(page_title = "Dashboard", layout="wide")

st.title(f"Welcome, {st.session_state.username}")
st.caption(f"Role: {st.session_state.role}")

if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.switch_page("Home.py")

st.subheader("System Overview")

try:
    df_incidents = get_all_incidents()

    if not df_incidents.empty:
        active_incidents = len(df_incidents[df_incidents['status'] != 'Closed'])
        resolved_incidents = len(df_incidents[df_incidents['status'] == 'Closed'])
    else:
        active_incidents = 0
        resolved_incidents = 0

except Exception as e:
    st.error(f"Database Error: {e}")
    active_incidents, resolved_incidents = 0, 0

col1, col2, col3 = st.columns(3)

col1.metric("System Status", "Online", "Stable")
col2.metric("Active Incidents", active_incidents, "Critical") 
col3.metric("Resolved Incidents", resolved_incidents)

st.divider()
st.info("Navigate to **Analytics** for charts or **Settings** to manage records.")