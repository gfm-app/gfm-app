import telebot


def menu_principal():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = telebot.types.KeyboardButton("💼 Mi cuenta")
    btn2 = telebot.types.KeyboardButton("💰 Balance")
    btn3 = telebot.types.KeyboardButton("👥 Referidos")
    btn4 = telebot.types.KeyboardButton("💸 Retirar")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    return markup
