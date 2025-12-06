import pandas as pd
from db import connect_database
import sqlite3

def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents (date, incident_type, severity, status, description, reported_by) VALUES (?, ?, ?, ?, ?, ?)""",
        (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY id DESC", conn
    )
    conn.close()
    return df

def update_incident_status(incident_id, new_status: str):
    """ Update the status of an existing cyber incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cyber_incidents SET status = ? WHERE id = ?""",
        (new_status, incident_id)
    )
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def delete_incident(incident_id: int):
    """ Delete an incident by ID."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM cyber_incidents WHERE id = ?""",
        (incident_id,)
    )
    row_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return row_affected > 0