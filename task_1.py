import time

from telebot import TeleBot, types


TOKEN = '5142087260:AAEZRe6ZUP3Ng9vDiUoIF5PI7zEnJsFd1eQ'

bot = TeleBot(TOKEN, parse_mode='HTML')


def seconds_to_time_str(seconds: int):
    minutes, seconds = divmod(seconds, 60)
    return '{:02}:{:02}'.format(minutes, seconds)


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    data = message.text.split()
    if len(data) == 1 or not data[1].isdigit():
        seconds = 60
    else:
        seconds = int(data[1])
    #seconds = 60
    chat_id = message.chat.id
    text = seconds_to_time_str(seconds)
    message = bot.send_message(chat_id, text)
    t1 = time.time()
    while seconds != 0:
        if time.time() - t1 >= 1:
            seconds -= 1
            t1 = time.time()

            bot.edit_message_text(
                text=seconds_to_time_str(seconds),
                chat_id=chat_id,
                message_id=message.id
            )


bot.polling()
