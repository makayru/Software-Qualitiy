# logger.py
import sqlite3
import datetime

class LoggerDatabaseManager:
    def __init__(self, db_name='logs.db'):
        self.db_name = db_name
        self.init_db()
        self.current_user = None
        self.limit = 10
        self.offset = 0

    def set_current_user(self, username):
        self.current_user = username

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        time TEXT,
                        username TEXT,
                        activity TEXT,
                        additional_info TEXT,
                        suspicious TEXT)''')
        conn.commit()
        conn.close()

    def log_activity(self, activity, additional_info=''):
        username = self.current_user
        suspicious = self.is_suspicious_activity(username, activity)
        now = datetime.datetime.now()
        query = '''INSERT INTO logs (date, time, username, activity, additional_info, suspicious) 
                   VALUES (?, ?, ?, ?, ?, ?)'''
        params = (now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), username, activity, additional_info, suspicious)
        self.execute_query(query, params)

    def execute_query(self, query, params):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
        conn.close()

    def is_suspicious_activity(self, username, activity):
        # Example criteria for suspicion
        if activity == 'login attempt' and self.check_failed_logins(username) > 5:
            return 'Yes'
        if activity == 'data access' and self.access_volume(username) > 1000:
            return 'Yes'
        if self.is_blacklisted_ip(self.get_user_ip(username)):
            return 'Yes'
        if self.is_out_of_normal_hours():
            return 'Yes'
        return 'No'

    def check_failed_logins(self, username):
        # Mock function to check failed login attempts
        return 6  # Example: return a number greater than the threshold

    def access_volume(self, username):
        # Mock function to check the volume of accessed data
        return 1200  # Example: return a number greater than the threshold

    def is_blacklisted_ip(self, ip):
        # Mock function to check if the IP is blacklisted
        blacklisted_ips = ['192.168.1.1', '10.0.0.1']
        return ip in blacklisted_ips

    def get_user_ip(self, username):
        # Mock function to get the user's IP address
        return '192.168.1.1'  # Example: return a blacklisted IP
    
    def is_out_of_normal_hours(self):
        # Mock function to check if the current time is outside normal hours
        current_hour = datetime.datetime.now().hour
        return current_hour < 6 or current_hour > 18
    
    def format_logs(self, logs):
        formatted_logs = []
        print()
        for log in logs:
            date, time, username, activity, additional_info, suspicious = log
            log_entry = (
                f"Date: {date}\n"
                f"Time: {time}\n"
                f"Username: {username}\n"
                f"Activity: {activity}\n"
                f"Additional Info: {additional_info}\n"
                f"Suspicious: {suspicious}\n"
                "-------------------------"
            )
            formatted_logs.append(log_entry)
        return formatted_logs
    
    def count_logs(self):
        query = '''SELECT COUNT(*) FROM logs'''
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(query)
        total_logs = c.fetchone()[0]
        conn.close()
        return total_logs

    def fetch_logs(self, limit=10, offset=0):
        query = '''SELECT date, time, username, activity, additional_info, suspicious FROM logs ORDER BY id DESC LIMIT ? OFFSET ?'''
        params = (limit, offset)
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(query, params)
        rows = c.fetchall()
        conn.close()
        return rows
    
    def display_logs(self, limit=10, offset=0):
        logs = self.fetch_logs(limit, offset)
        formatted_logs = self.format_logs(logs)
        for log in formatted_logs:
            print(log)

    def next_logs(self):
        total_logs = self.count_logs()
        if self.offset + self.limit < total_logs:
            self.offset += self.limit
        else:
            print("No more logs to display.")
        self.display_logs(self.limit, self.offset)

    def previous_logs(self):
        if self.offset - self.limit >= 0:
            self.offset -= self.limit
        else:
            print("You are already at the first log.")
            self.offset = 0
        self.display_logs(self.limit, self.offset)

    
    def logs_menu(self):
        while True:
            print("1. Next logs")
            print("2. Previous logs")
            print("3. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                self.next_logs()
            elif choice == '2':
                self.previous_logs()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
