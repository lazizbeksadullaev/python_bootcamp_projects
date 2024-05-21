import config

import telebot

from app.models import BotUser
from app.templates import Keys

import tests
import commands
from call_types import CallTypes
from states import States


bot = telebot.TeleBot(
    token=config.TOKEN,
    num_threads=3,
    parse_mode='HTML',
)


@bot.message_handler(content_types=['text'])
def message_handler(message):
    chat_id = message.chat.id
    user, success = BotUser.objects.get_or_create(chat_id=chat_id)
    if success:
        full_name = message.chat.first_name
        if message.chat.last_name:
            full_name += ' ' + message.chat.last_name

        user.full_name = full_name
        user.save()

    if message.text in Keys.CANCEL.getall():
        commands.cancel_command_handler(bot, message)
        return

    if (state := user.bot_state):
        if state == States.ENTER_TEST_NUMBER:
            tests.enter_test_number_message_handler(bot, message)

        return

    if message.text == '/start':
        commands.start_command_handler(bot, message)
    elif message.text == '/menu':
        commands.menu_command_handler(bot, message)
    elif message.text == '/cancel':
        commands.cancel_command_handler(bot, message)
    elif message.text == Keys.LANGUAGE.get(BotUser.Lang.UZ):
        user.lang = BotUser.Lang.UZ
        user.save()
        commands.menu_command_handler(bot, message)
    elif message.text == Keys.LANGUAGE.get(BotUser.Lang.RU):
        user.lang = BotUser.Lang.RU
        user.save()
        commands.menu_command_handler(bot, message)
    elif message.text in Keys.BACK.getall():
        commands.menu_command_handler(bot, message)
    elif message.text in Keys.TESTS_LIST.getall():
        tests.tests_list_message_handler(bot, message)
    elif message.text in Keys.SOLVE_TEST.getall():
        tests.solve_test_message_handler(bot, message)


callback_query_handlers = {
    CallTypes.TestStart: tests.test_start_call_handler,
    CallTypes.TestOneOption: tests.test_one_option_call_handler,
    CallTypes.TestOnePage: tests.test_one_page_call_handler,
    CallTypes.TestFinish: tests.test_finish_call_handler,
    CallTypes.TestBestResults: tests.test_best_results_call_handler,
    CallTypes.Test: tests.test_call_handler,
    CallTypes.TestResults: tests.test_results_call_handler,
    CallTypes.TestsListPage: tests.tests_list_page_call_handler,
}


@bot.callback_query_handler(func=lambda _: True)
def callback_query_handler(call):
    call_type = CallTypes.parse_data(call.data)
    for CallType, query_handler in callback_query_handlers.items():
        if call_type.__class__.__name__ == CallType.__name__:
            query_handler(bot, call)
            break


if __name__ == "__main__":
    # bot.polling()
    bot.infinity_polling()
