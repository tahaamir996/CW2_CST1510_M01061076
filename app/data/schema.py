import sqlite3
from .db import connect_database

def create_users_table(conn):
    """
    Args: 
    conn: Database connection object
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    );
    """
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
    print("Users table created successfully!")

# Test: Create the users table
conn = connect_database()
create_users_table(conn)
conn.close()

def create_cyber_incidents_table(conn):
    """
    Create the cyber_incidents table.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        incident_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT NOT NULL,
        description TEXT,
        reported_by TEXT,
        FOREIGN KEY (reported_by) REFERENCES users(username)
    );
    """

    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
    print("Cyber Incidents table created!")

def create_datasets_metadata_table(conn):
    """
    Create the datasets_metadata table.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        source TEXT,
        size INTEGER,
        category TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
    print("Datasets Metadata table created!")

def create_it_tickets_table(conn):
    """
    Create the it_tickets table.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        priority TEXT,
        status TEXT,
        assigned_to TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
    print("IT Tickets table created!")

def create_all_tables(conn):
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    print("\n All tables created successfully!")

conn = connect_database()
create_all_tables(conn)
conn.close()

