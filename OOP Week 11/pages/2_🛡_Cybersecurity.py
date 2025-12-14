import streamlit as st
import pandas as pd
from datetime import date
from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident

st.set_page_config(page_title="Incident Management", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

with st.sidebar:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.switch_page("Home.py")

st.title("⚙️ Incident Management")

db = DatabaseManager("database/platform.db")

with st.expander("🚀 Load Sample Data", expanded=False):
    if st.button("Load Data"):
        try:
            df = pd.read_csv("incidents.csv", encoding='latin1')
            count = 0
            for _, row in df.iterrows():
                itype = row.get('Type') or row.get('incident_type') or 'Intrusion'
                desc = row.get('Description') or 'No description'
                
                db.execute_query("""
                    INSERT INTO security_incidents (incident_type, severity, status, description)
                    VALUES (?, ?, ?, ?)
                """, (itype, "Medium", "Open", desc))
                count += 1
            st.success(f"Successfully loaded {count} records!")
            st.rerun()
        except Exception as e:
            st.error(f"Error loading file: {e}")

st.divider()

st.subheader("Report New Incident")

with st.form("add_incident_form"):
    col1, col2 = st.columns(2)
    with col1:
        i_type = st.selectbox("Type", ["Phishing", "Malware", "DDoS", "Intrusion", "Espionage", "Financial Theft"])
        i_severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    with col2:
        i_status = st.selectbox("Status", ["Open", "Investigating", "Resolved", "Closed"])
        i_date = st.date_input("Date", date.today())

    i_desc = st.text_area("Description")

    if st.form_submit_button("Submit Report", type="primary"):
        full_desc = f"[{i_date}] {i_desc} (Reported by {st.session_state.get('username', 'Admin')})"
        
        db.execute_query("""
            INSERT INTO security_incidents (incident_type, severity, status, description) 
            VALUES (?, ?, ?, ?)
        """, (i_type, i_severity, i_status, full_desc))

        st.success("Incident reported successfully!")
        st.rerun()

st.divider()

st.subheader("Update Incident Status")

rows = db.fetch_all("SELECT id, incident_type, severity, status, description FROM security_incidents")
incidents = [SecurityIncident(*row) for row in rows]

if incidents:
    incident_ids = [i.get_id() for i in incidents]
    selected_id = st.selectbox("Select Incident ID", incident_ids)

    current_incident = next((i for i in incidents if i.get_id() == selected_id), None)

    if current_incident:
        st.info(f"Selected: **{current_incident.get_type()}** | Status: **{current_incident.get_status()}**")

        with st.form("update_status_form"):
            st.write("New Status")
            new_status = st.selectbox("", ["Open", "Investigating", "Resolved", "Closed"], label_visibility="collapsed")
            
            if st.form_submit_button("Update Status"):
                db.execute_query("UPDATE security_incidents SET status = ? WHERE id = ?", 
                                (new_status, selected_id))
                
                st.success(f"Incident {selected_id} updated to {new_status}")
                st.rerun()
else:
    st.info("No incidents found in the database.")