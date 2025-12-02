import pandas as pd 
from pathlib import Path
import sqlite3
import os
from app.data.db import connect_database, DB_PATH
from app.data.schema import create_all_tables
from app.services.user_service import migrate_users_from_file

def load_csv_to_db(csv_name: str, table_name: str, conn: sqlite3.Connection):
    """Load a CSV file into a database table using pandas."""
    csv_path = Path("DATA") / csv_name

    if not csv_path.exists():
        print(f"Warning: {csv_path} not found. Skipping.")
        return 0
    
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(csv_path)
    
        # Clean column names (remove extra whitespace)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        df.to_sql(table_name, conn, if_exists='append', index=False)

        print(f"Loaded {len(df)} rows from {csv_name} into '{table_name}'.")
        return len(df)
    except Exception as e:
        print(f"Error loading {csv_name}: {e}")
        return 0

def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """
    print("\n" +"=" * 60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Old database '{Path(DB_PATH).name}' removed for a clean start.")
        print("       Connected")
    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    
    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)
    print("       Tables created.")
    conn.close()

    # Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file() 
    print(f"       Migrated {user_count} users")

    # Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    conn = connect_database() 
    total_rows = 0
    total_rows += load_csv_to_db(csv_name="cyber_incidents.csv", table_name="cyber_incidents", conn=conn)
    total_rows += load_csv_to_db(csv_name="datasets_metadata.csv", table_name="datasets_metadata", conn=conn)
    total_rows += load_csv_to_db(csv_name="it_tickets.csv", table_name="it_tickets", conn=conn)
    print(f"Total CSV rows loaded: {total_rows}")

    # Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()

    # Count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")

    conn.close()

    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n Database location: {DB_PATH.resolve()}")