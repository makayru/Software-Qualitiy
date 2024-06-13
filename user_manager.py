import sqlite3
import hashlib
from encryption import RSAEncryption

class UserManager:
    def __init__(self, encryption):
        self.conn = sqlite3.connect('unique_meal.db')
        self.cursor = self.conn.cursor()
        self.encryption = encryption
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username BLOB UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def hash_password(self, password):
        """Hash a password for storing."""
        salt = "unique_salt"  # In a real application, use a unique salt for each user
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest()

    def register_user(self, username, password, role):
        """Register a new user with hashed and encrypted data."""
        encrypted_username = self.encryption.encrypt_data(username)
        print(f"Registering User: {username} Encrypted: {encrypted_username}")  # Debugging statement
        password_hash = self.hash_password(password)
        try:
            self.cursor.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                                (encrypted_username, password_hash, role))
            self.conn.commit()
            print(f"User {username} registered successfully.")
        except sqlite3.IntegrityError:
            print("Error: Username already exists.")

    def authenticate_user(self, username, password):
        """Authenticate a user."""
        encrypted_username = self.encryption.encrypt_data(username)
        print(f"Authenticating User: {username} Encrypted: {encrypted_username}")  # Debugging statement
        sql = 'SELECT password_hash, role FROM users WHERE username = ?'
        self.cursor.execute(sql, (encrypted_username,))
        user = self.cursor.fetchone()
        print(f"Fetched User: {user}")  # Debugging statement
        if user:
            stored_password_hash, role = user
            if stored_password_hash == self.hash_password(password):
                print(f"Authentication successful. Role: {role}")
                return True
            else:
                print("Authentication failed. Incorrect password.")
                return False
        else:
            print("Authentication failed. User not found.")
            return False

    def close(self):
        self.conn.close()
