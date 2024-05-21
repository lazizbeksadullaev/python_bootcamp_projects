from math import factorial
import random

from telebot import TeleBot


TOKEN = '5339482047:AAFaUR_Zet3KVL14ZX7boBA6GHprgUDRF94'

bot = TeleBot(TOKEN, parse_mode='HTML')


def get_random_sum_digits(x):
    s = 0
    while x != 0:
        y = random.randint(0, min(9, x))
        s = s*10 + y
        x -= y

    return s


@bot.message_handler(commands=['number'])
def number_command_handler(message):
    data = message.text.split()
    if len(data) == 1 or not data[1].isdigit():
        number = random.randint(1, 100)
    else:
        number = min(1000, int(data[1]))

    text = str(get_random_sum_digits(number))
    bot.send_message(message.chat.id, text)


bot.polling()
