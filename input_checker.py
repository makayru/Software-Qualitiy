import re
import sqlite3
import random
import member_manager as MemberManager
from encryption import RSAEncryption

from StaticMethods import StaticMethods as SM 



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

def validate_fname_or_lname_input(prompt):
    while True:
        name = input(prompt)
        if re.match(r"^[a-zA-Z]+(?:[-' ]?[a-zA-Z]+)*$", name):
            return name
        else:
            print("Invalid input. Name should only contain letters, apostrophes, hyphens, and spaces.")

def connect_db():
    conn = sqlite3.connect('unique_meal.db')
    return conn

def validate_and_get_unique_username(prompt):
    while True:
        username = input(prompt)
        errors = []

        if len(username) < 8 or len(username) > 10:
            errors.append("Username must be between 8 and 10 characters.")
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9\'._]*$', username):
            errors.append("Username can only start with a letter or underscore, and can contain letters, numbers, underscores, apostrophes, and periods.")
        
        if not errors:
            rowid = SM.GetRowIDUsers(connect_db().cursor(), username)
            if rowid == None:
                print("Username is valid and unique.")
                return username
            else:
                errors.append("Username is already taken. Please choose another.")
                print("Invalid Username:")
                for error in errors:
                    print(error)
        else:
            print("Invalid Username:")
            for error in errors:
                print(error)
        errors.clear()
    
        

def validate_password_input(prompt):
    while True:
        password = input(prompt)
        errors = []

        if len(password) < 12 or len(password) > 30:
            errors.append("Password must be between 12 and 30 characters.")
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit.")
        if not re.search(r'[~!@#$%&_\-=+`|\\(){}[\]:;\'<>,.?/]', password):
            errors.append("Password must contain at least one special character.")

        if not errors:
            return RSAEncryption().hash_data(password)
            
        else:
            print("Invalid Password:")
            for error in errors:
                print(error)
        
        errors.clear()

def validate_role_input(prompt):
    while True:
        role = input(prompt)
        if role in ['Consultant', 'SystemAdmin']:
            return role
        else:
            print("Invalid input. Please enter a valid role.")

def generate_temp_password():
    length = 12

    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    special_characters = '!@#$%^&*(),.?":{}|<>'

    password_chars = [
        random.choice(lowercase),          # Add a random lowercase letter
        random.choice(uppercase),          # Add a random uppercase letter
        random.choice(digits),             # Add a random digit
        random.choice(special_characters)  # Add a random special character
    ]

    all_characters = lowercase + uppercase + digits + special_characters
    password_chars += random.choices(all_characters, k=length-4) #fill the rest of the password with random characters

    random.shuffle(password_chars)
    
    return ''.join(password_chars)

def reset_password(username):
    temp_password = generate_temp_password()
    print(f"Temporary password for {username}: {temp_password}")
    input("\nThis is a temporary password. Please change it after logging in. Press Enter to continue...")
    return RSAEncryption().hash_data(temp_password)

def reset_password_Consultant(username):
    conn = connect_db()
    cursor = conn.cursor()

    rowiduser = SM.GetRowIDUsers(cursor, username)
    rowidcon = SM.GetRowIDRole(cursor, username, 'consultants')
    if rowiduser != None and rowidcon != None: 
        hashed_passw = reset_password(username)
        sql = 'UPDATE consultants SET password = ? WHERE rowid = ?'
        sql2 = 'UPDATE users SET password = ? WHERE rowid = ?'
        cursor.execute(sql, (hashed_passw, rowidcon))
        cursor.execute(sql2, (hashed_passw, rowiduser))
        conn.commit()
        input("Password reset successful. Press Enter to return...")
        conn.close()
        return True
    else:
        input("Username not found. Password reset failed. Press Enter to return...")
        conn.close()
        return False


def reset_password_SystemAdmin(username):
    conn = connect_db()
    cursor = conn.cursor()

    rowiduser = SM.GetRowIDUsers(cursor, username)
    rowidSA = SM.GetRowIDRole(cursor, username, 'system_admins')
    if rowiduser != None and rowidSA != None:
        hashed_passw = reset_password(username)
        sql = 'UPDATE system_admins SET password = ? WHERE rowid = ?'
        sql2 = 'UPDATE users SET password = ? WHERE rowid = ?'
        cursor.execute(sql, (hashed_passw, rowidSA))
        cursor.execute(sql2, (hashed_passw, rowiduser))
        conn.commit()
        input("Password reset successful. Press Enter to return...")
        conn.close()
        return True
    else:
        input("Username not found. Password reset failed. Press enter to return...")
        conn.close()
        return False
    