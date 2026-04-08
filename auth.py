import json
import os
import hashlib

USERS_FILE = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def register_user(username, password, name):
    users = load_users()
    if username in users:
        return False, "❌ Username already exists! Please choose another."
    users[username] = {
        "name": name,
        "password": hash_password(password)
    }
    save_users(users)
    return True, "✅ Account created successfully! Please login."

def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, None, "❌ Username not found!"
    if users[username]["password"] != hash_password(password):
        return False, None, "❌ Incorrect password!"
    return True, users[username]["name"], "✅ Login successful!"