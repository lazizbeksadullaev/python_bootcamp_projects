import itertools
import os
import random
import string
from collections import defaultdict

import telebot
from django.db.models import Max, ObjectDoesNotExist
from telebot import types

import utils
import commands
from app.models import (BotUser, Question, Test, TestOne, TestResult,
                        TestResultOne)
from app.templates import Keys, Messages, Smiles
from call_types import CallTypes
from states import States


APP_DIR = 'app'
TESTS_PER_PAGE = 10


def get_best_test_result(user, test):
    max_solved = TestResult.results.filter(user=user, test=test) \
                           .aggregate(max_solved=Max('solved'))['max_solved']
    if not max_solved:
        max_solved = 0

    return max_solved


def parse_tests(user, page):
    tests_info = str()
    lang = user.lang
    start = (page-1)*TESTS_PER_PAGE
    end = page*TESTS_PER_PAGE
    tests = Test.tests.all()[start:end]
    for test in tests:
        max_solved = get_best_test_result(user, test)
        test_info = Messages.TESTS_LIST_TEST_INFO.get(lang).format(
           test_id=test.id,
           max_solved=max_solved,
           test_title=test.title,
           questions_count=test.questions_count,
        )
        tests_info += test_info + '\n'

    return tests_info


def tests_list_message_handler(bot: telebot.TeleBot, message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    text = utils.text_to_fat(Keys.TESTS_LIST)
    page = 1
    tests_info = parse_tests(user, page)
    text += utils.text_to_double_line(tests_info)
    tests_count = Test.tests.count()
    has_next_page = page*TESTS_PER_PAGE + 1 <= tests_count
    call_type = CallTypes.TestsListPage(page=page)
    page_keyboard = utils.make_page_keyboard(has_next_page, call_type)
    bot.send_message(chat_id, text,
                     reply_markup=page_keyboard)


def tests_list_page_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    page = call_type.page
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    text = utils.text_to_fat(Keys.TESTS_LIST)
    tests_info = parse_tests(user, page)
    text += utils.text_to_double_line(tests_info)
    tests_count = Test.tests.count()
    has_next_page = page*TESTS_PER_PAGE + 1 <= tests_count
    call_type = CallTypes.TestsListPage(page=page)
    page_keyboard = utils.make_page_keyboard(has_next_page, call_type)
    bot.edit_message_text(
        chat_id=chat_id,
        text=text,
        message_id=call.message.id,
        reply_markup=page_keyboard
    )


def solve_test_message_handler(bot: telebot.TeleBot, message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    user.bot_state = States.ENTER_TEST_NUMBER
    user.save()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(Keys.CANCEL.get(lang))
    text = Messages.ENTER_TEST_NUMBER.get(lang)
    bot.send_message(chat_id, text,
                     reply_markup=keyboard)


def enter_test_number_message_handler(bot: telebot.TeleBot, message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    try:
        test_id = int(message.text)
        test = Test.tests.get(id=test_id)
    except (ValueError, ObjectDoesNotExist):
        text = Messages.NOT_FOUND_OR_EMPTY.get(lang)
        bot.send_message(chat_id, text)
    else:
        commands.cancel_command_handler(bot, message)
        send_test_info(bot, user, test)


def send_test_info(bot: telebot.TeleBot, user, test):
    lang = user.lang
    chat_id = user.chat_id
    results = TestResult.results.filter(user=user, test=test)
    if (result := results.last()):
        last_attempt_datetime = utils.datetime_to_utc5_str(result.created)
        max_solved = results.aggregate(max_solved=Max('solved'))['max_solved']
    else:
        last_attempt_datetime = Messages.NEVER.get(lang)
        max_solved = 0

    test_info = Messages.TEST_INFO.get(lang).format(
        title=test.title,
        duration=test.duration,
        questions_count=test.questions_count,
        max_solved=max_solved,
        last_attempt_time=last_attempt_datetime,
    )
    call_type = CallTypes.TestStart(test_id=test.id)
    call_data = CallTypes.make_data(call_type)
    start_button = types.InlineKeyboardButton(
        text=Keys.TEST_START.get(lang),
        callback_data=call_data,
    )
    call_type = CallTypes.TestBestResults(test_id=test.id)
    call_data = CallTypes.make_data(call_type)
    best_results_button = types.InlineKeyboardButton(
        text=Keys.TEST_BEST_RESULTS.get(lang),
        callback_data=call_data,
    )
    test_keyboard = types.InlineKeyboardMarkup()
    test_keyboard.add(start_button)
    test_keyboard.add(best_results_button)
    bot.send_message(chat_id, test_info,
                     reply_markup=test_keyboard)


def get_test_one_info(test_result: TestResult, test_one: TestOne, lang: str):
    question = test_one.question
    options_list = question.get_options(lang)
    options_info = str()
    for index, option in enumerate(options_list):
        letter = string.ascii_uppercase[index]
        option_info = Messages.TEST_ONE_OPTION_INFO.get(lang).format(
            letter=letter,
            option=option,
        )
        options_info += option_info + '\n'

    test_one_info = Messages.TEST_ONE_INFO.get(lang).format(
        test_number=test_one.number,
        test_title=test_one.test.title,
        remaining_time=utils.seconds_to_time_str(test_result.remaining_time),
        question_title=test_one.question.get_title(lang),
        options_info=options_info,
    )
    return test_one_info


def get_test_one_image_path(test_one: TestOne):
    return os.path.join(APP_DIR, test_one.question.image.name)


def make_test_one_keyboard(test_result: TestResult, test_one: TestOne, lang):
    question = test_one.question
    options = question.get_options(lang)
    test_one_keyboard = types.InlineKeyboardMarkup(row_width=5)
    for index, option in enumerate(options):
        option_selected = TestResultOne.objects.filter(
            test_result=test_result,
            test_one=test_one,
            option=option,
        ).exists()
        letter = string.ascii_uppercase[index]
        option_text = f'{Smiles.SELECTED} '*option_selected + str(letter)
        call_type = CallTypes.TestOneOption(
            test_result_id=test_result.id,
            test_one_id=test_one.id,
            option=index,
        )
        call_data = CallTypes.make_data(call_type)
        option_button = types.InlineKeyboardButton(
            text=option_text,
            callback_data=call_data
        )
        test_one_keyboard.add(option_button)

    test = test_result.test
    page = test_one.number
    has_next_page = page + 1 <= test.questions_count
    call_type = CallTypes.TestOnePage(
        test_result_id=test_result.id,
        page=test_one.number,
    )
    page_keyboard = utils.make_page_keyboard(has_next_page, call_type)
    test_one_keyboard.add(*itertools.chain(*page_keyboard.keyboard))
    test_one_buttons = []
    for number, test_one in enumerate(test.test_ones.all(), 1):
        if number > test.questions_count:
            break

        call_type = CallTypes.TestOnePage(
            test_result_id=test_result.id,
            page=test_one.number,
        )
        call_data = CallTypes.make_data(call_type)
        option_selected = TestResultOne.objects.filter(
            test_result=test_result,
            test_one=test_one,
        ).exists()
        text = f'{Smiles.SOLVED} '*option_selected + str(test_one.number)
        test_one_button = types.InlineKeyboardButton(
            text=text,
            callback_data=call_data,
        )
        test_one_buttons.append(test_one_button)

    test_one_keyboard.add(*test_one_buttons)

    call_type = CallTypes.TestFinish(test_result_id=test_result.id)
    call_data = CallTypes.make_data(call_type)
    test_finish_button = types.InlineKeyboardButton(
        text=Keys.TEST_FINISH.get(lang),
        callback_data=call_data
    )
    test_one_keyboard.add(test_finish_button)
    return test_one_keyboard


def send_test(bot: telebot.TeleBot, test: Test, user: BotUser):
    test_result = TestResult.results.create(test=test, user=user)
    test_one = test.test_ones.first()
    lang = user.lang
    test_one_info = get_test_one_info(test_result, test_one, lang)
    test_one_keyboard = make_test_one_keyboard(test_result, test_one, lang)
    test_one_image_path = get_test_one_image_path(test_one)
    chat_id = user.chat_id
    with open(test_one_image_path, 'rb') as photo:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=test_one_info,
            reply_markup=test_one_keyboard,
        )


def random_shuffle_test(test):
    all_questions_count = test.all_questions_count
    test_ones = list(test.test_ones.all())
    random.shuffle(test_ones)
    for test_one in test_ones:
        test_one.number += all_questions_count
        test_one.save()

    for test_number in range(1, all_questions_count+1):
        test_one = test_ones[test_number-1]
        test_one.number = test_number
        test_one.save()


def test_start_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    call_type = CallTypes.parse_data(call.data)
    test_id = call_type.test_id
    test = Test.tests.get(id=test_id)
    random_shuffle_test(test)
    send_test(bot, test, user)
    bot.delete_message(chat_id, call.message.id)


def send_test_result(bot: telebot.TeleBot, test_result: TestResult):
    test = test_result.test
    for test_one in test.test_ones.all():
        user_answers_list = TestResultOne.objects.filter(
            test_result=test_result,
            test_one=test_one
        ).values_list('option', flat=True)
        question = test_one.question
        if question.check_answers(user_answers_list):
            test_result.solved += 1

    test_result.save()

    user = test_result.user
    chat_id = user.chat_id
    lang = user.lang
    test_result_info = Messages.TEST_RESULT_INFO.get(lang).format(
        title=test.title,
        duration=test.duration,
        questions_count=test.questions_count,
        solved=test_result.solved,
    )
    call_type = CallTypes.TestResults(
        test_result_id=test_result.id,
        page=1,
    )
    call_data = CallTypes.make_data(call_type)
    test_results_button = types.InlineKeyboardButton(
        text=Keys.TEST_RESULTS.get(lang),
        callback_data=call_data,
    )
    call_type = CallTypes.TestBestResults(test_id=test.id)
    call_data = CallTypes.make_data(call_type)
    best_results_button = types.InlineKeyboardButton(
        text=Keys.TEST_BEST_RESULTS.get(lang),
        callback_data=call_data,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(test_results_button)
    keyboard.add(best_results_button)
    bot.send_message(chat_id, test_result_info,
                     reply_markup=keyboard)


def test_finish_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    call_type = CallTypes.parse_data(call.data)
    test_result_id = call_type.test_result_id
    test_result = TestResult.results.get(id=test_result_id)
    send_test_result(bot, test_result)
    bot.delete_message(chat_id=chat_id, message_id=call.message.id)


def test_one_option_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    call_type = CallTypes.parse_data(call.data)
    test_result_id = call_type.test_result_id
    test_result = TestResult.results.get(id=test_result_id)
    if test_result.finished:
        send_test_result(bot, test_result)
        bot.delete_message(chat_id=chat_id, message_id=call.message.id)
        return

    test_one_id = call_type.test_one_id
    test_one = TestOne.objects.get(id=test_one_id)
    option_index = call_type.option
    options = test_one.question.get_options(lang)
    option = options[option_index]
    if test_one.question.type == Question.Type.SINGLE:
        TestResultOne.objects.filter(
            test_result=test_result,
            test_one=test_one
        ).delete()

    test_result_one, sucess = TestResultOne.objects.get_or_create(
        test_result=test_result,
        test_one=test_one,
        option=option,
    )
    if not sucess:
        test_result_one.delete()

    test_one_info = get_test_one_info(test_result, test_one, lang)
    test_one_keyboard = make_test_one_keyboard(test_result, test_one, lang)
    test_one_image_path = get_test_one_image_path(test_one)
    with open(test_one_image_path, 'rb') as media:
        bot.edit_message_media(
            media=types.InputMediaPhoto(
                media=media,
                caption=test_one_info,
                parse_mode='HTML',
            ),
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=test_one_keyboard,
        )


def test_one_page_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    call_type = CallTypes.parse_data(call.data)
    test_result_id = call_type.test_result_id
    test_result = TestResult.results.get(id=test_result_id)
    if test_result.finished:
        send_test_result(bot, test_result)
        bot.delete_message(chat_id=chat_id, message_id=call.message.id)
        return

    test_number = call_type.page
    test = test_result.test
    test_one = test.test_ones.all()[test_number-1]
    test_one_info = get_test_one_info(test_result, test_one, lang)
    test_one_keyboard = make_test_one_keyboard(test_result, test_one, lang)
    test_one_image_path = get_test_one_image_path(test_one)
    with open(test_one_image_path, 'rb') as media:
        bot.edit_message_media(
            media=types.InputMediaPhoto(
                media=media,
                caption=test_one_info,
                parse_mode='HTML',
            ),
            chat_id=chat_id,
            message_id=call.message.id,
            reply_markup=test_one_keyboard,
        )


def parse_test_best_results(results_list: list[tuple[int, int]], lang: str):
    best_results_info = utils.text_to_fat(Keys.TEST_BEST_RESULTS.get(lang))
    results_info = str()
    for index, result in enumerate(results_list, 1):
        user_id, max_solved = result
        user = BotUser.objects.get(id=user_id)
        full_name = user.full_name
        result_info = Messages.TEST_BEST_RESULT_INFO.get(lang).format(
            index=index,
            full_name=full_name,
            max_solved=max_solved,
        )
        results_info += result_info + '\n'

    best_results_info += utils.text_to_double_line(results_info)
    return best_results_info


def test_best_results_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    test_id = call_type.test_id
    test = Test.tests.get(id=test_id)
    results = TestResult.results.filter(test=test)
    results_dict = defaultdict(int)
    for test_result in results:
        user = test_result.user
        results_dict[user.id] = max(results_dict[user.id], test_result.solved)

    results_list = []
    for user_id, max_solved in results_dict.items():
        results_list.append((user_id, max_solved))

    results_list.sort(key=lambda x: -x[1])
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    best_results_info = parse_test_best_results(results_list[:10], lang)
    call_type = CallTypes.Test(test_id=test.id)
    call_data = CallTypes.make_data(call_type)
    test_button = types.InlineKeyboardButton(
        text=f'{Smiles.TEST} {test.title}',
        callback_data=call_data,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(test_button)
    bot.edit_message_text(
        chat_id=chat_id,
        text=best_results_info,
        message_id=call.message.id,
        reply_markup=keyboard
    )


def test_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    call_type = CallTypes.parse_data(call.data)
    test_id = call_type.test_id
    test = Test.tests.get(id=test_id)
    results = TestResult.results.filter(user=user, test=test)
    if (result := results.last()):
        last_attempt_datetime = utils.datetime_to_utc5_str(result.created)
        max_solved = results.aggregate(max_solved=Max('solved'))['max_solved']
    else:
        last_attempt_datetime = Messages.NEVER.get(lang)
        max_solved = 0

    test_info = Messages.TEST_INFO.get(lang).format(
        title=test.title,
        duration=test.duration,
        questions_count=test.questions_count,
        max_solved=max_solved,
        last_attempt_time=last_attempt_datetime,
    )
    call_type = CallTypes.TestStart(test_id=test.id)
    call_data = CallTypes.make_data(call_type)
    start_button = types.InlineKeyboardButton(
        text=Keys.TEST_START.get(lang),
        callback_data=call_data,
    )
    call_type = CallTypes.TestBestResults(test_id=test.id)
    call_data = CallTypes.make_data(call_type)
    best_results_button = types.InlineKeyboardButton(
        text=Keys.TEST_BEST_RESULTS.get(lang),
        callback_data=call_data,
    )
    test_keyboard = types.InlineKeyboardMarkup()
    test_keyboard.add(start_button)
    test_keyboard.add(best_results_button)
    bot.edit_message_text(
        chat_id=chat_id,
        text=test_info,
        message_id=call.message.id,
        reply_markup=test_keyboard
    )


def get_test_one_result_info(test_result_one, lang):
    test_one = test_result_one.test_one
    question = test_one.question
    options_info = str()
    answer = question.get_answers(lang)[0]
    for index, option in enumerate(question.get_options(lang)):
        letter = string.ascii_uppercase[index]
        option_info = Messages.TEST_ONE_OPTION_INFO.get(lang).format(
            letter=letter,
            option=option,
        )
        if option == test_result_one.option and option != answer:
            option_info += f' {Smiles.NOT_SOLVED}'

        if option == answer:
            option_info += f' {Smiles.SOLVED}'

        options_info += option_info + '\n'

    test_one_result_info = Messages.TEST_RESULT_ONE_INFO.get(lang).format(
        test_number=test_one.number,
        question_title=question.get_title(lang),
        test_title=test_one.test.title,
        options_info=options_info
    )
    return test_one_result_info


def make_test_one_result_keyboard(test_result_one, lang):
    test_result = test_result_one.test_result
    test_one = test_result_one.test_one
    test = test_result.test
    page = test_one.number
    has_next_page = page + 1 <= test.questions_count
    call_type = CallTypes.TestResults(
        test_result_id=test_result.id,
        page=test_one.number,
    )
    page_keyboard = utils.make_page_keyboard(has_next_page, call_type)
    test_one_result_keyboard = types.InlineKeyboardMarkup(row_width=5)
    test_one_result_keyboard.add(*itertools.chain(*page_keyboard.keyboard))
    test_one_buttons = []
    for number, test_one in enumerate(test.test_ones.all(), 1):
        call_type = CallTypes.TestResults(
            test_result_id=test_result.id,
            page=test_one.number,
        )
        call_data = CallTypes.make_data(call_type)
        smiles = [f'{Smiles.NOT_SOLVED}', f'{Smiles.SOLVED}']
        test_result_one, _ = TestResultOne.objects.get_or_create(
            test_result=test_result,
            test_one=test_one,
        )
        question = test_one.question
        solved = question.check_answers([test_result_one.option])
        text = f'{smiles[solved]} {test_one.number}'
        test_one_button = types.InlineKeyboardButton(
            text=text,
            callback_data=call_data,
        )
        test_one_buttons.append(test_one_button)

    test_one_result_keyboard.add(*test_one_buttons)
    call_type = CallTypes.Test(test_id=test.id)
    call_data = CallTypes.make_data(call_type)
    test_button = types.InlineKeyboardButton(
        text=f'{Smiles.TEST} {test.title}',
        callback_data=call_data,
    )
    test_one_result_keyboard.add(test_button)
    return test_one_result_keyboard


def test_results_call_handler(bot: telebot.TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    lang = user.lang
    call_type = CallTypes.parse_data(call.data)
    test_result_id = call_type.test_result_id
    test_one_number = call_type.page
    test_result = TestResult.results.get(id=test_result_id)
    test = test_result.test
    test_one = TestOne.objects.get(test=test, number=test_one_number)
    test_result_one, _ = TestResultOne.objects.get_or_create(
        test_result=test_result,
        test_one=test_one,
    )
    test_one_result_info = get_test_one_result_info(test_result_one, lang)
    test_one_result_keyboard = None
    test_one_result_keyboard = make_test_one_result_keyboard(
        test_result_one, lang
    )
    bot.edit_message_text(
        chat_id=chat_id,
        text=test_one_result_info,
        message_id=call.message.id,
        reply_markup=test_one_result_keyboard
    )
