import telebot


TOKEN = '5142087260:AAEZRe6ZUP3Ng9vDiUoIF5PI7zEnJsFd1eQ'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start', 'help'])
def say_greetings(message):
    bot.send_message(message.chat.id, 'Echo botiga xush kelibsiz')

@bot.message_handler()
def echo(message):
    bot.send_message(message.chat.id, message.text)

bot.polling(none_stop=True)