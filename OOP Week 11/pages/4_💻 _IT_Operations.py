import streamlit as st
import pandas as pd
from services.database_manager import DatabaseManager
from models.it_ticket import ITTicket

st.set_page_config(page_title="IT Operations", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

with st.sidebar:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.switch_page("Home.py")

st.title("IT Operations Management")

db = DatabaseManager("database/platform.db")

db.execute_query("CREATE TABLE IF NOT EXISTS it_tickets (id INTEGER PRIMARY KEY, title TEXT, priority TEXT, status TEXT)")

st.subheader("Manage Tickets (Add / Delete)")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("**Add Ticket**")
        
        new_title = st.text_input("Title", placeholder="e.g. Server Offline")
        new_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        new_status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
        
        if st.button("Add Ticket"):
            if new_title:
                db.execute_query("""
                    INSERT INTO it_tickets (title, priority, status) 
                    VALUES (?, ?, ?)
                """, (new_title, new_priority, new_status))
                st.success("Ticket Added!")
                st.rerun()
            else:
                st.error("Title is required")

        st.divider()

        st.markdown("**Delete Ticket**")
        
        rows = db.fetch_all("SELECT id, title, priority, status FROM it_tickets")
        tickets = [ITTicket(*row) for row in rows]
        
        if tickets:
            ticket_ids = [t.get_id() for t in tickets]
            del_id = st.selectbox("Select Ticket ID", ticket_ids)
            
            if st.button("Delete Ticket"):
                db.execute_query("DELETE FROM it_tickets WHERE id = ?", (del_id,))
                st.success(f"Deleted Ticket ID {del_id}")
                st.rerun()
        else:
            st.info("No tickets to delete.")

st.subheader("it_tickets")

if tickets:
    data = [{
        "ticket_id": t.get_id(),
        "title": t.get_title(),
        "priority": t.get_priority(),
        "status": t.get_status()
    } for t in tickets]
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No tickets found.")
    if st.button("Load Sample Tickets"):
        db.execute_query("INSERT INTO it_tickets (title, priority, status) VALUES (?, ?, ?)", 
                        ("Wifi Down in Building A", "High", "Open"))
        db.execute_query("INSERT INTO it_tickets (title, priority, status) VALUES (?, ?, ?)", 
                        ("Printer Jammed", "Low", "Open"))
        st.rerun()