import os

def main_menu():
    os.system('cls')
    print("1. Sign In")
    print("2. Exit")
    return input("Choose an option: ")

def super_admin_menu():
    os.system('cls')
    print("\nSuper Admin Menu")
    print("1. View all users")
    print("2. Register new user")
    print("3. Edit user")
    print("4. Delete user")
    print("5. reset user password (temporary)")
    print("6. Backup and Restore")
    print("7. view Logs")
    print("8. Search Members")
    print("9. Exit")

    return input("Choose an option: ")



def system_admin_menu():
    os.system('cls')
    print("\nSystem Admin Menu")
    print("1. Update password")
    print("2. View users")
    print("3. Add user")
    print("4. Edit user")
    print("5. Delete user")
    print("6. Reset user password (temporary)")
    print("7. Backup and Restore")
    print("8. View logs")
    print("9. Search members")
    print("10. Exit")
    return input("Choose an option: ")

def consultant_menu():
    os.system('cls')
    print("\nConsultant Menu")
    print("1. Update password")
    print("2. Add member")
    print("3. Edit member")
    print("4. Search member")
    print("5. Exit")
    return input("Choose an option: ")

def default_menu():
    os.system('cls')
    print("\nDefault Menu")
    print("1. View profile")
    print("2. Update profile")
    print("3. Exit")
    return input("Choose an option: ")