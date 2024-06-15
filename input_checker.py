import re
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