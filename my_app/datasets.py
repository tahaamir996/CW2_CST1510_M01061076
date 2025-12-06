import pandas as pd
from .db import connect_database
import sqlite3

def get_all_datasets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df

def insert_dataset(name, source, category, size):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata (name, source, category, size) 
        VALUES (?, ?, ?, ?)""",
        (name, source, category, size))
    dataset_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return dataset_id