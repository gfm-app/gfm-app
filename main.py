

from keyboards import menu_principal
from config import TOKEN, ADMIN_ID
import sqlite3
import telebot
print("🔥 ARCHIVO EJECUTÁNDOSE")


bot = telebot.TeleBot(TOKEN)

# Estados de usuarios
user_states = {}

# -------------------------------
# BASE DE DATOS
# -------------------------------


def init_db():
    conn = sqlite3.connect("gfm_users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT,
        wallet TEXT,
        referrer TEXT,
        balance INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


# -------------------------------
# START
# -------------------------------
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username

    conn = sqlite3.connect("gfm_users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.execute(
            "INSERT INTO users (user_id, username, balance) VALUES (?, ?, ?)",
            (user_id, username, 0.0)
        )
        conn.commit()

    conn.close()

    bot.send_message(
        message.chat.id, "👋 Bienvenido a GFM Bot\nSelecciona una opción:")


# -------------------------------
# MI CUENTA
# -------------------------------
@bot.message_handler(func=lambda message: message.text == "💼 Mi cuenta")
def mi_cuenta(message):
    user_id = message.from_user.id
    username = message.from_user.username

    conn = sqlite3.connect("gfm_users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    resultado = cursor.fetchone()

    balance = resultado[0] if resultado else 0

    conn.close()

    bot.send_message(
        message.chat.id,
        f"👤 Usuario: @{username}\n💰 Balance: {balance}"
    )


# -------------------------------
# BALANCE
# -------------------------------
@bot.message_handler(func=lambda message: message.text == "💰 Balance")
def ver_balance(message):
    user_id = message.from_user.id

    conn = sqlite3.connect("gfm_users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    resultado = cursor.fetchone()

    balance = resultado[0] if resultado else 0

    conn.close()

    bot.send_message(
        message.chat.id,
        f"💰 Tu balance actual es: {balance}"
    )


# -------------------------------
# REFERIDOS
# -------------------------------
@bot.message_handler(func=lambda message: message.text == "👥 Referidos")
def referidos(message):
    user_id = message.from_user.id

    conn = sqlite3.connect("gfm_users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE referrer = ?", (user_id,))
    total = cursor.fetchone()[0]

    conn.close()

    bot_username = "GridFlowMining_bot"
    link = f"https://t.me/{bot_username}?start={user_id}"

    bot.send_message(
        message.chat.id,
        f"👥 Tus referidos: {total}\n\n🔗 Tu link:\n{link}"
    )


# -------------------------------
# RETIRAR
# -------------------------------
@bot.message_handler(func=lambda message: message.text == "💸 Retirar")
def retirar(message):
    user_id = message.from_user.id

    conn = sqlite3.connect("gfm_users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
    resultado = cursor.fetchone()

    conn.close()

    if not resultado or not resultado[0]:
        user_states[user_id] = "esperando_wallet"
        bot.send_message(
            message.chat.id, "💼 Ingresa tu wallet RED BEP20 para retirar:")

        bot.register_next_step_handler(msg, capturar_datos)
        return

    bot.send_message(
        message.chat.id,
        f"💸 Puedes retirar a esta wallet:\n\n{resultado[0]}"
    )


# -------------------------------
# PEDIR EMAIL
# -------------------------------
@bot.message_handler(commands=['email'])
def pedir_email(message):
    user_id = message.from_user.id

    user_states[user_id] = "esperando_email"

    bot.send_message(
        message.chat.id,
        "📧 Ingresa tu correo electrónico:"
    )


# -------------------------------
# CAPTURAR DATOS (EMAIL + WALLET)
# -------------------------------
@bot.message_handler(func=lambda message: message.from_user.id in user_states)
def capturar_datos(message):
    user_id = message.from_user.id
    text = message.text

    conn = sqlite3.connect("gfm_users.db")
    cursor = conn.cursor()

    if user_states[user_id] == "esperando_email":
        cursor.execute(
            "UPDATE users SET email = ? WHERE user_id = ?",
            (text, user_id)
        )
        bot.send_message(message.chat.id, "✅ Email guardado correctamente")


print("👉 Antes del main")

if __name__ == "__main__":

    try:
        print("🚀 Iniciando bot...")
        print("🔑 TOKEN:", TOKEN)

        init_db()

        print("✅ Bot OK, iniciando polling...")
        bot.infinity_polling()

    except Exception as e:
        import traceback
        print("❌ ERROR DETECTADO:")
        traceback.print_exc()
