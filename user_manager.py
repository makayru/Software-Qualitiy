import sqlite3

class UserManager:
    def __init__(self):
        self.conn = sqlite3.connect('unique_meal.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        ''')
        self.conn.commit()

        # Insert default accounts if they do not exist
        self.insert_default_accounts()

    def register_user(self, username, password, role):
        try:
            self.cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                                (username, password, role))
            self.conn.commit()
            print(f"User {username} registered successfully.")
        except sqlite3.IntegrityError:
            print("Error: Username already exists.")

    def authenticate_user(self, username, password):
        sql = 'SELECT password, role FROM users WHERE username = ?'
        self.cursor.execute(sql, (username,))
        user = self.cursor.fetchone()
        if user:
            stored_password, role = user
            if stored_password == password:
                print(f"Authentication successful. Role: {role}")
                return role
            else:
                print("Authentication failed. Incorrect password.")
                return None
        else:
            print("Authentication failed. User not found.")
            return None

    def insert_default_accounts(self):
        """Insert default accounts with predefined credentials if they do not exist."""
        default_accounts = [
            ("super_admin", "Admin_123?", "Super_Administrator"),
            ("system_admin", "SysAdmin_123?", "System_Admin"),
            ("consultant", "Consultant_123?", "Consultant")
        ]

        for username, password, role in default_accounts:
            self.cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                                    (username, password, role))
                self.conn.commit()
                print(f"Account {username} with role {role} inserted successfully.")
            else:
                print(f"Account {username} already exists.")

    def close(self):
        self.conn.close()
