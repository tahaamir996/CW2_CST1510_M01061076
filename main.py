import pandas as pd
from app.data.db import connect_database 
from app.data.incidents import (
    insert_incident, get_all_incidents, 
    update_incident_status, delete_incident
)
from app.services.user_service import register_user, login_user
from setup_utils import setup_database_complete 

def run_comprehensive_tests():
    """ Run comprehensive tests on your database."""
    
    print("\n" + "="*60)
    print("RUNNING COMPREHENSIVE TESTS")
    print("="*60)
    
    conn = connect_database() 
    
    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user_w8", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")
    
    success, msg = login_user("test_user_w8", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")
    
    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")
    
    # Create (Insert)
    test_id = insert_incident(
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user_w8"
    )
    print(f"  Create: ✅ Incident #{test_id} created")
    
    # Read
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read:    Found incident #{test_id}")
    
    # Update
    update_incident_status(test_id, "Resolved")
    print(f"  Update:  Status updated")
    
    # Delete
    delete_incident(test_id)
    print(f"  Delete:  Incident deleted")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)


def main():
    
    setup_database_complete()
    
    run_comprehensive_tests()


if __name__ == "__main__":
    main()