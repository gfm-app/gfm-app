import sqlite3


def usuario_existe(user_id):
    conn = sqlite3.connect("gfm_users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    conn.close()
    return user


def registrar_usuario(user_id, username):
    conn = sqlite3.connect("gfm_users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO usuarios (user_id, username, balance) VALUES (?, ?, ?)",
        (user_id, username, 0)
    )

    conn.commit()
    conn.close()
