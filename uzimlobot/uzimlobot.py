import telebot
from telebot import types
from check_word import check_word
from transliterate import transliterate

TOKEN = '5142087260:AAEKhjIUY8Ou5kNVgnMhpc-zB4S73mwMZjw'

bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message: types.Message):
    username = (
        message.from_user.username
    )  # Bu usul bilan foydalanuvchi nomini olishimiz mumkin
    xabar = f"Assalom alaykum, {username}\n"
    xabar += "O'zbekcha imlo so'zlar botiga xush kelibsiz!" \
            "Qanday yozuv turida so'z kiritmoqchisiz, tanlang: "
    keyboard = types.InlineKeyboardMarkup()
    options = [types.InlineKeyboardButton('cyrillic', callback_data='cyrillic'),
               types.InlineKeyboardButton('latin', callback_data='latin')]
    keyboard.add(*options)
    bot.send_message(message.chat.id, xabar, reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help_hadler(message: types.Message):
    bot.send_message(message.chat.id, "Ihtiyoriy so'zni yuboring, imlo bo'yicha tahlil qilamiz")

to_variant = ''
@bot.callback_query_handler(func=lambda message: True)
def call_handler(call: types.CallbackQuery):
    c = call.data
    global to_variant
    to_variant = c


@bot.message_handler()
def tekshir(message: types.Message):
    if to_variant == "cyrillic":
        word = message.text
        result = check_word(word)
        if result['available']:
            response = f"✅ {word.title()}"
        else:
            response = f"❌ {word.title()}\n"
            for text in result['matches']:
                response += f"✅ {text.title()}\n"

        bot.reply_to(message, response)
    else:
        word = transliterate(text=message.text, to_variant="cyrillic")
        result = check_word(word)
        if result['available']:
            response = f"✅ {transliterate(word, to_variant='latin').title()}"
        else:
            response = f"❌ {transliterate(word, to_variant='latin').title()}\n"
            for text in result['matches']:
                response += f"✅ {transliterate(text, to_variant='latin').title()}\n"

        bot.reply_to(message, response)

bot.polling()