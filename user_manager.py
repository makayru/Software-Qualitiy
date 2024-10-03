# user_manager.py
import sqlite3
import datetime
import logger as log
import os
import zipfile
from encryption import RSAEncryption

class UserManager:
    def __init__(self, logger):
        self.conn = sqlite3.connect('unique_meal.db')
        self.cursor = self.conn.cursor()
        self.logger = logger
        self.create_table()
        self.current_user = None

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
        # Fetch all encrypted usernames and passwords from the database
        sql = 'SELECT username, password, role FROM users'
        self.cursor.execute(sql)
        users = self.cursor.fetchall()
        
        # Hash the input password
        hashed_input_password = RSAEncryption.hash_data(password)
    
        # Iterate through users and attempt decryption/authentication
        for encrypted_username, stored_password, role in users:
            try:
                decrypted_username = RSAEncryption.decrypt_data(encrypted_username)
            except Exception as e:
                print(f"Decryption failed: {str(e)}")
                continue  # Skip this entry if decryption fails
            
            if decrypted_username == username and stored_password == hashed_input_password:
                self.current_user = username
                print(f"Authentication successful. Role: {role}")
                self.logger.log_activity('login attempt', 'Successful')
                return role
        
        # If no match was found
        print("Authentication failed. User not found or incorrect password.")
        self.logger.log_activity('login attempt', 'Failed: User not found or incorrect password')
        return None


    

    def insert_default_accounts(self):
        """Insert default accounts with predefined credentials if they do not exist."""
        default_accounts = [
            (RSAEncryption.encrypt_data("super_admin"), RSAEncryption.hash_data("Admin_123?"), "Super_Administrator"),
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

    def create_backup(self):
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = os.path.join(backup_dir, f'backup_{timestamp}.zip')

        with zipfile.ZipFile(backup_filename, 'w') as backup_zip:
            backup_zip.write('unique_meal.db')
            backup_zip.write('logs.db')

        self.logger.log_activity(f"Created backup_{timestamp}.zip", "Successful")

    def close(self):
        self.conn.close()
