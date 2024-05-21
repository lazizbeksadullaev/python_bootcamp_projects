import datetime
from email.mime import message

from telebot import TeleBot


TOKEN = '5142087260:AAEZRe6ZUP3Ng9vDiUoIF5PI7zEnJsFd1eQ'

bot = TeleBot(TOKEN, parse_mode='HTML')
def check(message):
    birthday = list(map(int, message.text.split('/')))
    current_time = datetime.datetime.now()
    left_time = datetime.datetime(current_time.year, birthday[1], birthday[2]) - current_time
    text = str(left_time)
    bot.send_message(message.chat.id, text)
@bot.message_handler(func=check)
@bot.message_handler(commands=['start'])
def start_command_handler(message):
    bot.send_message(message.chat.id, "Tug'ilgan kuningizni yyyy/mm/dd formatida kiriting:")
    #year = datetime.datetime.now().year
    #new_year = datetime.datetime(year+1, 1, 1)
    #text = str(new_year - datetime.datetime.now())
    #bot.send_message(message.chat.id, text)


bot.polling()
