import bcrypt
import os 

USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    try:
        password_bytes = plain_text_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except ValueError:
        return False
    
def user_exists(username):
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f.readlines():
                user, _ = line.strip().split(',', 1)
                if user == username:
                    return True
        return False
    except FileNotFoundError:
        return False
    
def register_user (username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    hashed_password = hash_password(password)

    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed_password}\n")
    print(f"Success: User '{username}' registered successfully!")
    return True

def login_user(username, password):
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f.readlines():
                user, stored_hash = line.strip().split(',', 1)

                if user == username:
                    if verify_password(password, stored_hash):
                        print(f"Success: Welcome, {username}!")
                        return True
                    else:
                        print("Error: Invalid password.")
                        return False
            print("Error: Username not found.")
            return False
    except FileNotFoundError:
        print("Error: username not found")
        return False
    
def validate_username(username):
    if not 4 <= len(username) <= 14:
        return (False, "Username must be between 4 and 14 characters.")
    return (True, "")
def validate_password(password):
    if len(password) < 8:
        return (False, "Password should have 8 or more characters.")
    if not any(char.isdigit() for char in password):
        return (False, "Password should have atleast one digit.")
    if not any(char.isalpha() for char in password):
        return (False, "Password should have atleast one letter.")
    return (True, "")

# step 11 
def display_menu():
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFOR")
    print( "Secure Authentication System")
    print("="*50)
    print("\n [1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            register_user(username, password)

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                input("\nPress Enter to return to main menu...")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1,2, or 3.")

if __name__ == "__main__":
    main()

