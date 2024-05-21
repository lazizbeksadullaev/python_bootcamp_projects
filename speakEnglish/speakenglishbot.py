import telebot
from googletrans import Translator
from oxfordfind import get_definition
from telebot import types

TOKEN = '5142087260:AAEKhjIUY8Ou5kNVgnMhpc-zB4S73mwMZjw'

bot = telebot.TeleBot(token=TOKEN)
tarjimon = Translator()


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Bizga ihtiyoriy so'z yoki matn yuboring sizga uni tarjimasini qaytaramiz")


@bot.message_handler(commands=['help'])
def hel_handler(message):
    text = "Agar yuborgan so'zingiz 1 yoki 2 ta so'z uzunligida bo'lsa uni ma'nolari" \
           " bilan qaytaramiz 2 so'zdan ortiq matn yuborsangiz uni tarjimasi qaytariladi"
    text += """Bunda matn kiritilgan til avtomatik\
 aniqlanadi
    """  # 3 tirnoq va oddiy 1 tirnoqlarda qanday qilib uzun matn kiritish ni ko'rdik
    bot.send_message(message.chat.id, text=text)


@bot.message_handler()
def habar_handler(message: types.Message):
    til = tarjimon.detect(message.text).lang
    if len(message.text.split()) >= 2:
        dest = 'uz' if til == 'en' else 'en'
        tarjima = tarjimon.translate(text=message.text, dest=dest).text
        bot.reply_to(message=message, text=tarjima)
    else:
        if til == 'en':
            word_id = message.text
        else:
            word_id = tarjimon.translate(text=message.text, dest='en').text

        lookup = get_definition(word_id=word_id)
        if lookup:
            bot.reply_to(message, f"Word: '{word_id}'\nDefinitions:\n{lookup['definitions']}")
            if lookup.get('audio'):
                bot.send_audio(message.chat.id, audio=lookup['audio'])
        else:
            bot.reply_to(message, "Bunday so'z topilmadi")


bot.polling()
