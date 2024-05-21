import telebot
import requests
import time
import exchangetest

TOKEN = '5142087260:AAEZRe6ZUP3Ng9vDiUoIF5PI7zEnJsFd1eQ'

bot = telebot.TeleBot(TOKEN)

#currency = {}
#buttons = telebot.types.InlineKeyboardMarkup(row_width=3)
buttons = telebot.types.InlineKeyboardMarkup(row_width=2)
keyString = ''
valueString = ''


@bot.message_handler(commands=['start', 'help'])
def give_info(message):
    if message.text == '/start':
        text = '''Valyuta kurslari botiga xush kelibsiz!!!
Bu botda turli valyuta kurslari ayirboshlash 
narxlarini ko'rib olishingiz mumkin! Marhamat qilib 
quyidagi xalqaro valyutalar orasidan 
taqqoslamoqchi bo'lgan dastlabki pul birligingizni
tanlang va buni 1 birlik deb
hisoblaymiz misol uchun 1 USD = ? kabi >>>'''
        bot.send_message(message.chat.id, text=text)
        chatId = message.chat.id
        time.sleep(3)
        for index in range(0, len(exchangetest.get_supported_currencies()) - 2, 2):#3):
            key = exchangetest.get_supported_currencies()[index][0]
            value = exchangetest.get_supported_currencies()[index][1]

            key1 = exchangetest.get_supported_currencies()[index + 1][0]
            value1 = exchangetest.get_supported_currencies()[index + 1][1]

            #key2 = exchangetest.get_supported_currencies()[index + 2][0]
            #value2 = exchangetest.get_supported_currencies()[index + 2][1]
            buttons.add(telebot.types.InlineKeyboardButton(value, callback_data=key),
                        telebot.types.InlineKeyboardButton(value1, callback_data=key1))
                        #telebot.types.InlineKeyboardButton(value2, callback_data=key2))

        bot.send_message(chatId, "Xalqaro valyutalar menyusi:", reply_markup=buttons)
    if message.text == '/help':
        text = '''
        Biz sizga 1 A davlat puli = X B davlat puliga\ntengligini hisoblab beramiz:
        '''
        bot.send_message(message.chat.id, text=text)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global keyString
    global valueString
    if keyString != '':
        valueString = call.data
        url2 = f'https://v6.exchangerate-api.com/v6/{exchangetest.API_KEY}/pair/{keyString}/{valueString}'
        response = requests.get(url2)
        value = response.json()
        result = f"{value['time_last_update_utc']} holatiga ko'ra\n 1 {keyString} = {value['conversion_rate']} {valueString} ga teng"
        bot.send_message(call.message.chat.id, text=result)
        keyString = ''
        valueString = ''
    else:
        keyString = call.data
        chatId = call.message.chat.id
        bot.send_message(chatId, f"Marhamart qilib yuqoridagi ro'yxatdan keyingi taqqoslamoqchi bo'lgan valyutangizni kiriting yani 1 {keyString} = ?")


# if call.data == '1':
#     bot.send_message(chat_id=call.message.chat.id,text="1")
# if call.data == '2':
#     bot.send_message(chat_id=call.message.chat.id,text="2")
# if call.data == '3':
#     bot.send_message(chat_id=call.message.chat.id,text="3")


@bot.message_handler()
def work(message):
        bot.send_message(message.chat.id, f'Pul birliklarini tanlashda xato bo\'ldi, \n/start buyruqidan qayta boshlang yoki \n/help dan yordam oling')

bot.polling(none_stop=True)
