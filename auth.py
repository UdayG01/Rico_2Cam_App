import sqlite3
import bcrypt
import os

DB_FILENAME = "app_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()

    # Create default admin user if the table was just created or if empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        default_hash = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', ("admin", default_hash))
        conn.commit()
    
    conn.close()

def register_user(username, password):
    if not username.strip() or not password.strip():
        return False, "Username and password cannot be empty."

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username.strip(), hashed_pw))
        conn.commit()
        return True, "User registered successfully."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    except Exception as e:
        return False, f"Error: {e}"
    finally:
        if 'conn' in locals():
            conn.close()

def verify_login(username, password):
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username.strip(),))
        row = cursor.fetchone()
        if row:
            stored_hash = row[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                return True, "Login successful."
            else:
                return False, "Invalid password."
        return False, "User not found."
    except Exception as e:
        return False, f"Server Error: {e}"
    finally:
        if 'conn' in locals():
            conn.close()
