import telebot
import time

TOKEN = '5142087260:AAEZRe6ZUP3Ng9vDiUoIF5PI7zEnJsFd1eQ'

bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start', 'help'])
def say_greetings(message):
    text = 'Echo botiga xush kelibsiz'
    bot.send_message(message.chat.id, text=text)
@bot.message_handler()
def echo(message):
    '''try:
        son = int(message.text)
        bot.send_message(message.chat.id, str(factorial(son)))
    except:
        bot.send_message(message.chat.id, 'factorial hisoblash uchun butun musbat son kiring')'''
    text = message.text
    bot.send_message(message.chat.id, text)
bot.polling(none_stop=True)

while True: # Don't let the main Thread end.
    pass