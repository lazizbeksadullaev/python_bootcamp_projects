from telebot import TeleBot, types
#from aiogram import Message


TOKEN = '5142087260:AAEZRe6ZUP3Ng9vDiUoIF5PI7zEnJsFd1eQ'

bot = TeleBot(token=TOKEN, parse_mode='HTML')

@bot.message_handler()
def message_handler(message):
    chat_id = message.chat.id
    text = f'Your user ID: <b>{message.from_user.id}</b>\n'
    text +=f'Current chat ID: <b>{message.chat.id}</b>'
    
    if message.forward_from != None:
        text +=f'\nForwarded from: <b>{message.forward_from.id}</b>'
    
    bot.send_message(message.chat.id, text)
bot.infinity_polling()