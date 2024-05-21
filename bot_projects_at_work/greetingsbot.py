import telebot
from telebot import types
from pprint import pprint as print

TOKEN = "5142087260:AAEKhjIUY8Ou5kNVgnMhpc-zB4S73mwMZjw"
bot = telebot.TeleBot(TOKEN)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
keyboard.add('Button1', 'Button2', 'Button3', 'Button4', 'Button5')
keyboard.add('Button6', 'Button7', 'Button8', 'Button9')
keyboard.add('Button10', 'Button11', 'Button12')
keyboard.add('Button13', 'Button14')
keyboard.add('Button15')
# keyboard = types.ReplyKeyboardRemove()

# keyboard = types.InlineKeyboardMarkup()# inline keyboard yasaw uchn dastlab markup
# # bilan keyboard yasab olamiz, keyin add.button bilan button qo'shamiz
# keyboard.add(types.InlineKeyboardButton(text='determinants guruhi', url='https://t.me/+8MNU88UOfBdiZjYy'))
# keyboard.add(types.InlineKeyboardButton(text='cpython.uz sayti', url='https://cpython.uz'))
# keyboard.add(types.InlineKeyboardButton(text='Lazizbek Sadullaev', url='tg://user?id=797871413'))
# bot.send_message(chat_id=-1001550009252, text="klaviatura", reply_markup=keyboard)
text1 = """
<b> jirni </b>
<i> kursiv </i>
<u> underline </u>
<s>strikethrough (specifies no longer correct)</s>
<code>print(123)</code>
<code>print(12345)</code>
<a href='cpython.uz'>cpython.uz</a>
"""
chatid = -1001550009252
# message1 = bot.send_message(chat_id=chatid, text=text1, parse_mode='HTML')
# Use this method to send text messages.
# On success, the sent Message(obj) is returned.
# message1 nomli yuborilgan message obyekti qaytariladi
# print('bot.send_message metodi message1 nomli message obyektini qayatardi: message1 = ')
# print(message1.json)
# print(message1.id)
message2 = bot.forward_message(chat_id=chatid, from_chat_id=chatid, message_id=381)
with open('photo_2022-10-07_14-03-25.jpg', 'rb') as photo1:
    bot.send_photo(chat_id=chatid, photo=photo1, caption='Bu google ning CEO si')
print(message2.id)
# bot.edit_message_text('Bu yerda doim bir tekstdan foydalanyapmiz', chat_id=chatid, message_id=400)

message3 = bot.send_message(chat_id=chatid, text="Salom kursdoshlarim")

print(type(message3))
print(message3.json)
print(message3.chat.id) # message3.json['chat']['id']=message3.chat.id
print(message3.json['chat']['id'])
# print(message3.chat.id)
print(type(message3.from_user))#message3.from qila olmimiz chunki from python ni kalit so'zi
# shuning uchun message3.from_user ishlatiladi va u bizga User obyektini qayataradi ekan
# print(message3.json dan chiuvchi from kalitiga qarang boshqa dict(obyekt) kelgan
print(message3.from_user.is_bot)
print(message3.from_user.username)
print(message3.json['chat'])
bot.reply_to(message=message2, text='Yoshligida katta qiyinchilikla bo\'gan 0 dan boshlagan')
@bot.message_handler(commands=['start'])
def start_message_handler(message):
    print(message.from_user.first_name)

@bot.message_handler(content_types=['left_chat_member'])
def left_member(message):
    print(message.json)
    print(message.left_chat_member.first_name)

@bot.message_handler(content_types=['new_chat_members'])
def new_member(message):
    print(message.json)
    print(message.new_chat_members)
bot.send_poll(chat_id=chatid, question='Kim Turkiyani 1-marta bosib olgan', type='quiz', options=['a', '1', 'b'], is_anonymous=False, correct_option_id=1)

keyboard = types.ReplyKeyboardMarkup()
keyboard.add(types.KeyboardButton('Kontakni yuborish', request_contact=True))
keyboard.add(types.KeyboardButton('Lokatsiyani yuboring', request_location=True))
bot.send_message(chat_id=chatid, text='Danillani yuboring', reply_markup=keyboard)


# @bot.message_handler(func=lambda message: message.text.isdigit())
# def handler(message):
#     print(message.text, message.chat.id, message.id)


# def iseven(a):
#     return True if a % 2 == 0 else False
#
#
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")
#
#
# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


bot.polling()
