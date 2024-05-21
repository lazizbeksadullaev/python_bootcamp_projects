import telebot
from telebot import types
from currency_data import compare_currencies

TOKEN = '5142087260:AAEKhjIUY8Ou5kNVgnMhpc-zB4S73mwMZjw'
CURRENCIES = ["USD", "RUB", "KZT", "EUR", "GBP", "UZS"]

bot = telebot.TeleBot(token=TOKEN)


def get_currencies():
    currencies = []
    for i in CURRENCIES:
        button = types.InlineKeyboardButton(text=i, callback_data=i)
        currencies.append(button)

    return currencies


def get_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    deletes = [types.InlineKeyboardButton(text="C", callback_data="clear"),
               types.InlineKeyboardButton(text='x', callback_data='x')]
    keyboard.add(*deletes)

    buttons = []
    for i in reversed(range(10)):
        button = types.InlineKeyboardButton(text=str(i),
                                            callback_data=str(i))
        buttons.append(button)
    keyboard.add(*buttons)

    keyboard.add(*get_currencies())

    keyboard.add(types.InlineKeyboardButton(text='qancha',
                                            callback_data='qancha'))

    keyboard.add(types.InlineKeyboardButton(text='hisobla',
                                            callback_data='hisobla'))
    return keyboard


def calc(text):
    # text = 23 USD qancha USZ
    splited_text = text.split(' ')
    value = float(splited_text[0])
    base_currency = splited_text[1]
    target_currency = splited_text[3]

    return compare_currencies(value, base_currency, target_currency)


@bot.message_handler(commands=['start', 'help'])
def start_handler(message):
    text1 = "Qaysi valyutalarni o'zaro taqqoslamoqchisiz? "
    bot.send_message(chat_id=message.chat.id, text=text1)

    keyboard = get_keyboard()
    bot.send_message(chat_id=message.chat.id, text='0', reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    keyboard = get_keyboard()
    c = call.data
    text = call.message.text
    if c == 'clear':
        text = '0'
    elif c == 'x':
        if len(text) >= 3:
            old_call = text[-3] + text[-2] + text[-1]
            if old_call in CURRENCIES:
                text = text[:-3]
            else:
                text = text[:-1]
        else:
            if len(text) <= 1:
                text = '0'
            else:
                text = text[:-1]
    elif c in CURRENCIES:
        text += f' {c} '
    elif c == 'qancha':
        text += f' {c}'
    elif text == '0' and c.isdigit():
        text = c
    elif c == 'hisobla':
        print(text)

        try:
            text = text + f"\n{str(calc(text))}"
            # bot.send_message(call.message.chat.id, text1)
        except:
            text = '0'
    else:
        text += c

    # 2. pollingni tagida edit_message haqida tushuntrishlarni o'qing
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=keyboard)
    except:
        pass


bot.polling()
