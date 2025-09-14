import json, os, getpass
from werkzeug.security import generate_password_hash

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_users(u):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=2)

def main():
    users = load_users()
    username = input("Admin username: ").strip()
    if username in users:
        print("User exists. Exiting.")
        return
    password = getpass.getpass("Admin password: ")
    password2 = getpass.getpass("Confirm password: ")
    if password != password2:
        print("Passwords don't match. Exiting.")
        return
    users[username] = {
        "password": generate_password_hash(password),
        "role": "admin"
    }
    save_users(users)
    print(f"Admin {username} created.")

if __name__ == "__main__":
    main()
