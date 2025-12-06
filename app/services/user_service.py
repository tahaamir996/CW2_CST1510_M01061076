import bcrypt
from pathlib import Path
from app.data.users import get_user_by_username, insert_user

DEFAULT_MIGRATION_PATH = Path("LAB Week7") / "users.txt"

def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    if get_user_by_username(username):
        return False, f"User '{username}' already exists."

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'),
                                  bcrypt.gensalt()
                                  ).decode('utf-8')

    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."

def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    
    # Verify password
    stored_hash = user[2] 
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, f"Login successful!"
    return False, "Incorrect password."

def migrate_users_from_file(filepath: Path = DEFAULT_MIGRATION_PATH):
    """Migrate users from text file to database (migration logic)."""
    users_migrated = 0

    try:
        if not filepath.exists():
            print(f"Warning: {filepath} not found. Skipping migration.")
            return 0
        
        with filepath.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines[1:]:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 2:
                continue

            username = parts[0]
            password_hash = parts[1]
            role = parts[2] if len(parts) >= 3 else "user"

            if get_user_by_username(username) is None:
                insert_user(username, password_hash, role)
                users_migrated += 1
            else:
                print(f"User '{username}' already exists. Skipping.")

    except Exception as e:
        print(f"An error occurred during migration: {e}")

    return users_migrated 