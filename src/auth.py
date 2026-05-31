import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


DB_PATH = "database/users.db"


def create_users_table():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def register_user(name, email, password):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    hashed_password = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, hashed_password)
    )

    connection.commit()
    connection.close()


def verify_user(email, password):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    connection.close()

    if user and check_password_hash(user[3], password):
        return user

    return None