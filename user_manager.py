# user_manager.py
import sqlite3
import datetime
import logger as log
import os
import zipfile
from encryption import RSAEncryption
import shutil

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
        self.current_user = username
        sql = 'SELECT password, role FROM users WHERE username = ?'
        self.cursor.execute(sql, (username,))
        user = self.cursor.fetchone()
        if user:
            stored_password, role = user
            if stored_password == RSAEncryption.hash_data(self, password):
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
            (f"super_admin", RSAEncryption.hash_data(self, "Admin_123?"), "Super_Administrator"),
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
        
    def list_backup_files(self):
        backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups')
        
        # List backup files in the 'backups' directory
        backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.zip')]
        
        if not backup_files:
            print("No backup ZIP files found in the 'backups' directory.")
            return None
        
        print("Available backup files:")
        for i, backup_file in enumerate(backup_files, start=1):
            print(f"{i}. {backup_file}")
        
        # Prompt user to select a backup file
        while True:
            try:
                choice = int(input("Enter the number of the backup file to restore: "))
                if 1 <= choice <= len(backup_files):
                    selected_backup = backup_files[choice - 1]
                    return os.path.join(backup_dir, selected_backup)
                else:
                    print("Invalid choice. Please enter a number within the range.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    def restore_backup(self):
        backup_file = self.list_backup_files()
        if not backup_file:
            return
        
        main_directory = os.path.dirname(os.path.abspath(__file__))  # Assuming UserManager is in main directory
        db_file = os.path.join(main_directory, 'unique_meal.db')
        
        try:
            # Connect to SQLite database
            connection = sqlite3.connect(db_file)
            cursor = connection.cursor()

            # Open the backup ZIP file
            with zipfile.ZipFile(backup_file, 'r') as backup_zip:
                for file_info in backup_zip.infolist():
                    if file_info.filename.endswith('.sql'):
                        with backup_zip.open(file_info) as sql_file:
                            sql_statements = sql_file.read().decode('utf-8')
                            cursor.executescript(sql_statements)
                            print(f"Executed SQL statements from {file_info.filename}")

            # Commit changes and close connection
            connection.commit()
            connection.close()
            print("Database restored successfully.")

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        except zipfile.BadZipFile:
            print(f"Invalid ZIP file: {backup_file}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if connection:
                connection.close()
    
    def close(self):
        self.conn.close()
