import streamlit as st
import plotly.express as px
import pandas as pd
from incidents import get_all_incidents  

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.title("Incident Analytics")

df = get_all_incidents()

if not df.empty:
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
            st.plotly_chart(fig2, use_container_width = True)

    with st.expander("View Raq Data Table"):
        st.dataframe(df, use_container_width = True)

else:
    st.warning("No incidents found in the database.")