import sqlite3
import secrets
import string
from getpass import getpass


# Initialize database connection
def init_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            domain TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn, cursor

# Function to generate a random password
def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Function to view passwords with limited authentication attempts
def view_passwords(cursor):
    master_password = "almighty password"
    attempts = 5
    for attempt in range(attempts):
        user_input = getpass("Enter the master password: ")
        if user_input == master_password:
            cursor.execute("SELECT domain, password FROM passwords")
            records = cursor.fetchall()
            print("\nStored Passwords:")
            print("Domain".ljust(20) + " | Password")
            print("-" * 40)
            for domain, password in records:
                print(f"{domain.ljust(20)} | {password}")
            return
        else:
            print(f"Incorrect password. Attempts left: {attempts - attempt - 1}")
    print("Too many incorrect attempts.")
    exit()

# Function to create and store a new password, with options for manual or secure password generation
def create_password(cursor, conn):
    domain = input("Enter the domain/service name: ")
    gen_choice = input("Do you want to (G)enerate a secure password or (T)ype your own? ").strip().lower()
    if gen_choice == 'g':
        new_password = generate_password()
        print(f"Generated secure password for {domain}.")
    elif gen_choice == 't':
        new_password = getpass("Enter your password (hidden): ")
    else:
        print("Invalid choice. Returning to main menu.")
        return
    
    cursor.execute("INSERT INTO passwords (domain, password) VALUES (?, ?)", (domain, new_password))
    conn.commit()
    print(f"Password for {domain} has been stored.")

# Function to delete a password for a given domain
def delete_password(cursor, conn):
    domain = input("Enter the domain/service name to delete: ")
    cursor.execute("SELECT * FROM passwords WHERE domain = ?", (domain,))
    record = cursor.fetchone()
    if record:
        confirm = input(f"Are you sure you want to delete the password for '{domain}'? (Y/N): ").strip().lower()
        if confirm == 'y':
            cursor.execute("DELETE FROM passwords WHERE domain = ?", (domain,))
            conn.commit()
            print(f"Password for {domain} has been deleted.")
        else:
            print("Deletion cancelled.")
    else:
        print(f"No password found for domain '{domain}'.")

def main():
    conn, cursor = init_db()

    while True:
        choice = input("\nDo you want to (V)iew, (C)reate, or (D)elete a password? ").strip().lower()
        if choice == 'v':
            view_passwords(cursor)
        elif choice == 'c':
            create_password(cursor, conn)
        elif choice == 'd':
            delete_password(cursor, conn)
        else:
            print("Invalid choice. Please enter 'V' to view, 'C' to create, or 'D' to delete.")

if __name__ == "__main__":
    main()
