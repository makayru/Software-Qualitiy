import re
import sqlite3
import member_manager as MemberManager

cities = ["Amsterdam", "Rotterdam", "Utrecht", "The Hague", "Eindhoven", "Groningen", "Maastricht", "Leiden", "Delft", "Breda"]
def get_valid_int_input(prompt):
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

def get_valid_gender_input(prompt):
    while True:
        gender = input(prompt).upper()
        if gender in ['M', 'F']:
            return gender
        else:
            print("Invalid input. Please enter 'M' for male or 'F' for female.")
def get_valid_email_input(prompt):
    while True:
        email = input(prompt)
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return email
        else:
            print("Invalid email format. Please enter a valid email address.")
def get_valid_phone_input(prompt):
    while True:
        phone = input(prompt)
        if re.match(r"^\d{8}$", phone):
            return f"+31-6-{phone}"
        else:
            print("Invalid phone format. Please enter 8 digits (+31-6-DDDDDDDD).")
def get_valid_zip_code_input(prompt):
    while True:
        zip_code = input(prompt)
        if re.match(r"^\d{4}[A-Z]{2}$", zip_code):
            return zip_code
        else:
            print("Invalid zip code format. Please enter a valid zip code (DDDDXX).")
def get_valid_city_input(prompt):
    while True:
        try:
            city_index = int(input(prompt))
            if 1 <= city_index <= len(cities):
                return cities[city_index - 1]
            else:
                print(f"Invalid selection. Please enter a number between 1 and {len(cities)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def connect_db():
    conn = sqlite3.connect('unique_meal.db')
    return conn

def is_valid_username(username):
    if len(username) < 8 or len(username) > 10:
        return False, "Username must be between 8 and 10 characters"
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9\'._]*$', username):
        return False, "Username can only start with a letter or underscore, and can contain letters, numbers, underscores, apostrophes, and periods"
    return True, ""

def is_unique_username(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM members WHERE username = ?", (username,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def is_valid_password(password):
    if len(password) < 12 or len(password) > 30:
        return False, "Password must be between 12 and 30 characters"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    if not re.search(r'[~!@#$%&_\-=+`|\\(){}[\]:;\'<>,.?/]', password):
        return False, "Password must contain at least one special character"
    return True, ""