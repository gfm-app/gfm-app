
import sqlite3

DB_NAME = "gfm_users.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT UNIQUE,
        wallet TEXT UNIQUE,
        referrer INTEGER,
        balance REAL DEFAULT 0
     )
     """) 

    conn.commit()
    conn.close() 


def register_user(user_id, username, email, wallet):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (user_id, username, email, wallet, balance)
    VALUES (?, ?, ?, ?, 0)
    """, (user_id, username, email, wallet))

    conn.commit()
    conn.close()


def add_user(user_id, username, referrer=None):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username, referrer) VALUES (?, ?, ?)",
        (user_id, username, referrer)
    )

    conn.commit()
    conn.close()


def user_exists(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()

    conn.close()

    return user is not None


def get_balance(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return 0


def get_referrals(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE referrer=?", (user_id,))
    result = cursor.fetchone()

    conn.close()

    return result[0]











