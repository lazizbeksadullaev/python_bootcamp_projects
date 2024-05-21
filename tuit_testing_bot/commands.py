import telebot
from telebot import types

from app.models import BotUser
from app.templates import Messages, Keys


def start_command_handler(bot: telebot.TeleBot, message):
    chat_id = message.chat.id
    language_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    language_keyboard.add(Keys.LANGUAGE.get(BotUser.Lang.UZ))
    language_keyboard.add(Keys.LANGUAGE.get(BotUser.Lang.RU))
    text = Messages.START_COMMAND_HANDLER.text
    bot.send_message(chat_id, text,
                     reply_markup=language_keyboard)


def menu_command_handler(bot: telebot.TeleBot, message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_keyboard.add(Keys.SOLVE_TEST.get(lang), Keys.TESTS_LIST.get(lang))
    text = Messages.MENU_COMMAND_HANDLER.get(lang)
    bot.send_message(chat_id, text,
                     reply_markup=menu_keyboard)


def cancel_command_handler(bot: telebot.TeleBot, message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    user.bot_state = None
    user.save()
    menu_command_handler(bot, message)
