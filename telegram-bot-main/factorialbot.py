from math import factorial
import random

from telebot import TeleBot


TOKEN = '5142087260:AAEZRe6ZUP3Ng9vDiUoIF5PI7zEnJsFd1eQ'

bot = TeleBot(TOKEN, parse_mode='HTML')
@bot.message_handler(commands=['factorial'])
def number_command_handler(message):
    
    #son = data[1]
    try:
        habar = message.text
        son = habar[habar.find(' '):]
        natija = str(factorial(int(son)))
        bot.reply_to(message, natija)
    except:
        bot.reply_to(message, 'Natija oplib bo\'lmaydi son kiritishda xatolik bo\'ldi')

bot.polling()
