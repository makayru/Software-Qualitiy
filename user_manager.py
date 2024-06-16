# user_manager.py
import sqlite3
import datetime
import logger as log

class UserManager:
    def __init__(self, logger):
        self.conn = sqlite3.connect('unique_meal.db')
        self.cursor = self.conn.cursor()
        self.logger = logger
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            role TEXT NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY,
            member_id INTEGER NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            weight INTEGER NOT NULL,
            address TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultants (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            role TEXT NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_admins (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            role TEXT NOT NULL
        )
        ''')
        self.conn.commit()
        
        

        # Insert default accounts if they do not exist
        self.insert_default_accounts()

    def authenticate_user(self, username, password):
        sql = 'SELECT password, role FROM users WHERE username = ?'
        self.cursor.execute(sql, (username,))
        user = self.cursor.fetchone()
        if user:
            stored_password, role = user
            if stored_password == password:
                print(f"Authentication successful. Role: {role}")
                self.logger.log_activity('login attempt', 'Successful')
                return role
            else:
                print("Authentication failed. Incorrect password.")
                self.logger.log_activity('login attempt', 'Failed: Incorrect password')
                return None
        else:
            print("Authentication failed. User not found.")
            self.logger.log_activity('login attempt', 'Failed: User not found')
            return None

    def insert_default_accounts(self):
        """Insert default accounts with predefined credentials if they do not exist."""
        default_accounts = [
            ("super_admin", "Admin_123?", "Super_Administrator"),
        ]

        for username, password, role in default_accounts:
            self.cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('INSERT INTO users (username, password, first_name, last_name, registration_date, role) VALUES (?, ?, ?, ?, ?, ?)',
                                    (username, password,"", "", "", role))
                self.conn.commit()
                print(f"Account {username} with role {role} inserted successfully.")
                self.logger.log_activity("insert default account", "Successful")
            else:
                print(f"Account {username} already exists.")
                self.logger.log_activity( "insert default account", "Failed: Already exists")

    def close(self):
        self.conn.close()
