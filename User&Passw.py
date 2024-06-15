import sqlite3
import re

# Function to connect to SQLite database
def connect_db():
    conn = sqlite3.connect('unique_meal.db')
    return conn

# Function to check if username is valid
def is_valid_username(username):
    # Check length
    if len(username) < 8 or len(username) > 10:
        return False, "Username must be between 8 and 10 characters"
    # Check characters and starting character
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9\'._]*$', username):
        return False, "Username can only start with a letter or underscore, and can contain letters, numbers, underscores, apostrophes, and periods"
    return True, ""

# Function to check if password is valid
def is_valid_password(password):
    # Check length
    if len(password) < 12 or len(password) > 30:
        return False, "Password must be between 12 and 30 characters"
    # Check required characters
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    if not re.search(r'[~!@#$%&_\-=+`|\\(){}[\]:;\'<>,.?/]', password):
        return False, "Password must contain at least one special character"
    return True, ""

# Function to check if username is unique
def is_unique_username(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM members WHERE username = ?", (username,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

# Example function to register a new user
def register_user(username, password):
    is_valid, error_message = is_valid_username(username)
    if not is_valid:
        return error_message
    
    if not is_unique_username(username):
        return "Username already exists"
    
    is_valid, error_message = is_valid_password(password)
    if not is_valid:
        return error_message
    
    # Add user to database (example using SQLite)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO members (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return "User registered successfully"

# Example usage
if __name__ == "__main__":
    # Test registration
    username = "test_user"
    password = "StrongPassword123!"
    result = register_user(username, password)
    print(result)
