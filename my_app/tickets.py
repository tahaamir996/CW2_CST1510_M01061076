import pandas as pd
from .db import connect_database
import sqlite3

def get_all_tickets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY created_date DESC", conn)
    conn.close()
    return df

def update_ticket_priority(ticket_id: int, new_priority: str):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE it_tickets SET priority = ? WHERE id = ?""",
        (new_priority, ticket_id))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0