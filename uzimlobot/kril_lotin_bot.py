import telebot
from telebot import types
from transliterate import transliterate

TOKEN = '5142087260:AAEKhjIUY8Ou5kNVgnMhpc-zB4S73mwMZjw'
bot = telebot.TeleBot(token=TOKEN)

# \start komandasi uchun mas'ul funksiya
@bot.message_handler(commands=["start"])
def send_welcome(message):
    username = (
        message.from_user.username
    )  # Bu usul bilan foydalanuvchi nomini olishimiz mumkin
    xabar = f"Assalom alaykum, {username} Kirill-Lotin-Kirill botiga xush kelibsiz!"
    xabar += "\nQaysi funksiyadan foydalanmoqchiligingizni tanlang:"

    keyboard = types.InlineKeyboardMarkup()
    options = [types.InlineKeyboardButton('latin_to_cyrillic', callback_data='cyrillic'),
               types.InlineKeyboardButton('cyrillic_to_latin', callback_data='latin')]
    keyboard.add(*options)
    bot.send_message(message.chat.id, xabar, reply_markup=keyboard)

to_variant = ''
@bot.callback_query_handler(func=lambda message: True)
def call_handler(call: types.CallbackQuery):
    c = call.data
    global to_variant
    to_variant = c
    print(c)

# matnlar uchun mas'ul funksiya
@bot.message_handler(func=lambda msg: msg.text is not None)
def translate(message: types.Message):
    xabar = message.text
    global to_variant
    ugirilgan_xabar = transliterate(text=xabar, to_variant=to_variant)
    bot.reply_to(message, ugirilgan_xabar)

bot.polling()