import streamlit as st
import plotly.express as px
import pandas as pd
from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident

st.set_page_config(page_title="Data Science", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

with st.sidebar:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.switch_page("Home.py")

st.title("Incident Analytics")

db_manager = DatabaseManager("database/platform.db")
query = "SELECT id, incident_type, severity, status, description FROM security_incidents"
rows = db_manager.fetch_all(query)
incidents = [SecurityIncident(*row) for row in rows]

if incidents:
    data = [{
        'id': i.get_id(),
        'severity': i.get_severity(),
        'status': i.get_status(),
        'type': i.get_type()
    } for i in incidents]

    df = pd.DataFrame(data)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Incidents by Severity")
        if 'severity' in df.columns:
            chart_data = df['severity'].value_counts().reset_index()
            chart_data.columns = ['severity', 'count']

            fig = px.bar(chart_data, x='severity', y='count', color='severity', title="Severity Levels")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Status Distribution")
        if 'status' in df.columns:
            fig2 = px.pie(df, names='status', title="Current Status Split")
            st.plotly_chart(fig2, use_container_width=True)

    with st.expander("View Raq Data Table"):
        st.dataframe(df, use_container_width=True)

else:
    st.warning("No incidents found in the database.")