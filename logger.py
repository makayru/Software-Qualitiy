# logger.py
import sqlite3
import datetime

class LoggerDatabaseManager:
    def __init__(self, db_name='logs.db'):
        self.db_name = db_name
        self.init_db()
        self.current_user = None

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
