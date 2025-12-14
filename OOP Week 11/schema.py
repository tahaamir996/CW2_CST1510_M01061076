from services.database_manager import DatabaseManager

def create_users_table(db):
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
    """
    db.execute_query(query)
    print("Users table ready.")

def create_security_incidents_table(db):
    query = """
    CREATE TABLE IF NOT EXISTS security_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_type TEXT,
        severity TEXT,
        status TEXT,
        description TEXT
    )
    """
    db.execute_query(query)
    print("Security Incidents table ready.")

def create_datasets_table(db):
    query = """
    CREATE TABLE IF NOT EXISTS datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        source TEXT,
        size_bytes INTEGER,
        rows INTEGER
    )
    """
    db.execute_query(query)
    print("Datasets table ready.")

def create_it_tickets_table(db):
    query = """
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        priority TEXT,
        status TEXT,
        assigned_to TEXT
    )
    """
    db.execute_query(query)
    print("IT Tickets table ready.")

if __name__ == "__main__":
    print("Initializing Database Schema...")
    
    db_manager = DatabaseManager("database/platform.db")
    
    create_users_table(db_manager)
    create_security_incidents_table(db_manager)
    create_datasets_table(db_manager)
    create_it_tickets_table(db_manager)
