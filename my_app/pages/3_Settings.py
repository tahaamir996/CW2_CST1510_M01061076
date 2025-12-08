import streamlit as st
import pandas as pd
from incidents import insert_incident, get_all_incidents, update_incident_status 
from datetime import date

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("⛔ You must be logged in to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.title("⚙️ Incident Management")

with st.expander("🚀 Load Sample Data", expanded=False):
    st.write("Click this button to view Cyber Incidents Data.")

    if st.button("Load Data"):
        try:
            df = pd.read_csv("incidents.csv", encoding='latin1')

            count = 0
            for index, row in df.head(30).iterrows():
                p_type = row.get('Type') or row.get('incident_type') or 'Intrusion'
                p_date = row.get('Date') or str(date.today())
                p_desc = row.get('Description') or 'No description'
                
                insert_incident(
                    date=str(p_date),
                    incident_type=str(p_type),
                    severity="Medium",
                    status='Open',
                    description=str(p_desc),
                    reported_by=st.session_state.username
                )
                count += 1

            st.success(f"Successfully loaded {count} records!")
        except FileNotFoundError:
            st.error("File 'incidents.csv' not found.")
        except Exception as e:
            st.error(f"Error loading data: {e}")

st.divider()

st.subheader("Report New Incident")

with st.form("add_incident_form"):
    col1, col2 = st.columns(2)
    with col1:
        i_type = st.selectbox("Type", ["Phishing", "Malware", "DDoS", "Intrusion", "Espionage", "Financial Theft", "Sabotage"])
        i_severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    with col2:
        i_status = st.selectbox("Status", ["Open", "Investigating", "Resolved", "Closed"])
        i_data = st.date_input("Date", date.today())

    i_desc = st.text_area("Description")

    if st.form_submit_button("Submit Report", type="primary"):
        insert_incident(str(i_data), i_type, i_severity, i_status, i_desc, st.session_state.username)
        st.success("Incident logged successfully!")
        st.rerun()

st.divider()

st.subheader("Update Incident Status")
df_db = get_all_incidents()

if not df_db.empty and 'id' in df_db.columns:
    incident_ids = df_db['id'].tolist()
    selected_id = st.selectbox("Select Incident ID", incident_ids)
    
    current_row = df_db[df_db['id'] == selected_id].iloc[0]
    st.info(f"Selected: **{current_row['incident_type']}** | Status: **{current_row['status']}**")
    
    with st.form("update_form"):
        new_status = st.selectbox("New Status", ["Open", "Investigating", "Resolved", "Closed"])
        if st.form_submit_button("Update Status"):
            update_incident_status(selected_id, new_status)
            st.success("Status updated!")
            st.rerun()
else:
    st.info("No incidents found.")