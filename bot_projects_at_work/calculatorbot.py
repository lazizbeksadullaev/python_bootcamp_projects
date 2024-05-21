from telebot import TeleBot, types
from math import factorial

TOKEN='5142087260:AAEKhjIUY8Ou5kNVgnMhpc-zB4S73mwMZjw'
bot = TeleBot(token=TOKEN)
chatid = -1001550009252
# bot.send_message(chat_id=chatid, text='borr')
def get_digits():
    buttons = []
    for d in reversed(range(10)):
        button = types.InlineKeyboardButton(text=str(d), callback_data=str(d))
        buttons.append(button)

    return buttons

def get_operators():
    operators = []
    for op in ['+', '-', '*', '/', '//', '**', '(', ')', '!', '=']:
        button = types.InlineKeyboardButton(text=op, callback_data=op)
        operators.append(button)


    return operators

def get_keyboard_for_digit():
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    deletes = [types.InlineKeyboardButton(text="C", callback_data="clear"),
               types.InlineKeyboardButton(text='x', callback_data='x')]
    keyboard.add(*deletes)

    buttons = get_digits()
    for i in range(0, len(buttons), 3):
        keyboard.add(*buttons[i: i + 3])
    keyboard.add(*get_operators())

    return keyboard

def get_keyboard_for_operator():
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    deletes = [types.InlineKeyboardButton(text="C", callback_data="clear"),
               types.InlineKeyboardButton(text='x', callback_data='x')]
    keyboard.add(*deletes)

    buttons = get_digits()
    for i in range(0, len(buttons), 3):
        keyboard.add(*buttons[i: i + 3])

    qavslar = [types.InlineKeyboardButton('(', callback_data='('),
               types.InlineKeyboardButton(text=')', callback_data=')')]
    keyboard.add(*qavslar)

    return keyboard

def calc(expr):
    expr = list(expr)
    new_expr = str()
    son = str()

    for i in range(len(expr)):
        if expr[i] == '!':
            new_expr += f'factorial({son})'
            son = ''
        elif expr[i] in "+-/*":
            new_expr += son
            new_expr += expr[i]
            son = ''
        else:
            son += expr[i]
    new_expr += son # buni ko'p xatolik olib keyin qo'ydim chunki ohirgi
    # operatordan keyin yozilgan son new_expr ga qo'shilmay qolib ketar ekan
    return eval(new_expr)

@bot.message_handler(commands=['start'])
def start_handler(message):
    # 1. pastda InlineKeyboardButtonla uchun tushuntirishlar bor
    keyboard = get_keyboard_for_digit()
    text1 = '0'
    bot.send_message(message.chat.id, text1, reply_markup=keyboard)
    # print(keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    c = call.data
    text = call.message.text
    if c == 'clear':
        text = '0'
    elif c == 'x':
        text = text[:-1]
    elif text == '0' and c.isdigit():
        text = c
    elif c == '=':
        try:
            text = str(calc(text))
        except:
            text = '0'
    else:
        text += c

    if c.isdigit() or c == 'clear' or c in '()x!=':
        keyboard = get_keyboard_for_digit()
    else:
        keyboard = get_keyboard_for_operator()

    # 2. pollingni tagida edit_message haqida tushuntrishlarni o'qing
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=keyboard)
    except:
        pass




    # print(call.message.text)# inlinekeyboard yopishib kelgan messageni textini olib beradi
    # print(call.data)

bot.polling()
# 1. InlineKeyboardButtonlar haqida
# keyboard = types.InlineKeyboardMarkup(row_width=3)
    # keyboard.add(types.InlineKeyboardButton(text='button1', callback_data='1'))
    # keyboard.add(types.InlineKeyboardButton(text='button5', callback_data='5'))
    # keyboard.add(types.InlineKeyboardButton(text='button8', callback_data='8'))
    # keyboard.add(types.InlineKeyboardButton(text='button10', callback_data='10'))
    # harbir qator buttonlari tgbotda ham alohida qatorlarda yaratiladi
    # bot.send_message(chat_id=message.chat.id, text='0', reply_markup=keyboard)

# 2. edit_message() parametrlariga tushuntirishlar
"""
    bot.edit_message_text(text, call.message.chat.id, call.id) # call.id desak nechanchi id 
    # dagi message ga o'zgartrish kiritishi keraklikini berishimiz kerak edi, 
    # lekin call.id da message emas call ni topgani uchun bu csll ga edit kiritolmaydi
    bot.edit_message_text(text=text, chat_id=call.id, message_id=call.message.id)# desak esa,
    # chat_id ga biz call ni idisini berib yubordik, aslida bu chat qaysi id da ketyotganini kiriitsh
    # kerak bo'lgani uchun message.chat.id ni berishimiz keral.Demak eng to'g'ri varianti:
    # text=text, chat_id=call.message.chat.id, message_id=call.message.id ekan arglar
    """

# polling()-qandiy muammo yuzaga kelsihidan qatiy nazar to'xtidi
# polling(none_stop=True)-internet bn bo'gliq muammo yuzaga keganda tuxtamidi,
# lekin boshqa har qandiy xatolik hollada tuxtidi
# infinty_polling()-qanday muammo bo'lishidan qat'i nazar ishlab turadi use for deploying
