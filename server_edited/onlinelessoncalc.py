from telebot import TeleBot, types
from math import factorial


TOKEN = '5142087260:AAEZRe6ZUP3Ng9vDiUoIF5PI7zEnJsFd1eQ'
bot = TeleBot(token=TOKEN)


def get_digits():
    buttons = []
    for d in reversed(range(10)):
        button = types.InlineKeyboardButton(text=str(d),
                                            callback_data=str(d))
        buttons.append(button)

    return buttons


def get_operators():
    buttons = []
    op = '//'
    buttons.append(types.InlineKeyboardButton(text=op, callback_data=op))
    for op in '+-/*=!':
        buttons.append(types.InlineKeyboardButton(text=op,
                                                  callback_data=op))

    return buttons


def get_keyboard_for_operator():
    keyboard = types.InlineKeyboardMarkup(row_width=5)
    keyboard.add(types.InlineKeyboardButton(text='C',
                                            callback_data='C'))
    buttons = get_digits()
    for i in range(0, len(buttons), 3):
        keyboard.add(*buttons[i:i+3])
    
    keyboard.add(types.InlineKeyboardButton(text='(', callback_data='('))
    keyboard.add(types.InlineKeyboardButton(text=')', callback_data=')'))
    keyboard.add(types.InlineKeyboardButton(text='!', callback_data='!'))

    return keyboard


def get_keyboard_for_digit():
    keyboard = get_keyboard_for_operator()
    keyboard.add(*get_operators())
    return keyboard


@bot.message_handler(commands=['start'])
def start_handler(message):
    text = '0'
    keyboard = get_keyboard_for_digit()
    bot.send_message(message.chat.id, text,
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    c = call.data
    text = call.message.text
    if c == 'C':
        text = '0'
    elif text == '0' and c.isdigit():
        text = c
    else:
        if c == '=':
            #text = str(eval(text))
            try:
                text = str(eval(text))
            except Exception:
                text = '0'
        else:
            text += c

    if c.isdigit() or c == 'C' or c == '=' or c == '(' or c == ')':
        keyboard = get_keyboard_for_digit()
    else:
        keyboard = get_keyboard_for_operator()

    bot.edit_message_text(
        text=text,
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        reply_markup=keyboard,
    )


bot.polling(none_stop=True)


# polling
# polling(none_stop=True)
# infinity_polling