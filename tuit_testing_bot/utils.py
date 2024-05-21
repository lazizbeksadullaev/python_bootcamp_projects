import requests

import config
from call_types import CallTypes
from app.templates import Smiles

import telebot
from telebot import types

from django.utils import timezone

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


def seconds_to_time_str(seconds: int):
    minutes, seconds = seconds // 60, seconds % 60
    return '{:02}:{:02}'.format(minutes, seconds)


def text_to_fat(text: str) -> str:
    return f"<b>{text}</b>"


def text_to_italic(text: str) -> str:
    return f"<i>{text}</i>"


def text_to_code(text: str) -> str:
    return f"<code>{text}</code>"


def text_to_underline(text: str) -> str:
    return f"<u>{text}</u>"


def text_to_double_line(text: str) -> str:
    new_text = '\n———————————————————'
    new_text += '\n\n'
    new_text += text
    new_text += '———————————————————'
    new_text += '\n\n'
    return new_text


def datetime_to_utc5_str(dt) -> str:
    return (dt+timezone.timedelta(hours=5)).strftime('%d-%m-%Y, %H:%M')


def filter_tag(tag: Tag, ol_number=None):
    if isinstance(tag, NavigableString):
        text = tag
        text = text.replace('<', '&#60;')
        text = text.replace('>', '&#62;')
        return text

    html = str()
    li_number = 0
    for child_tag in tag:
        if tag.name == 'ol':
            if child_tag.name == 'li':
                li_number += 1
        else:
            li_number = None

        html += filter_tag(child_tag, li_number)

    format_tags = ['strong', 'em', 'pre', 'b', 'u', 'i', 'code']
    if tag.name in format_tags:
        return f'<{tag.name}>{html}</{tag.name}>'

    if tag.name == 'a':
        return f"""<a href="{tag.get("href")}">{tag.text}</a>"""

    if tag.name == 'li':
        if ol_number:
            return f'{ol_number}. {html}'
        return f'•  {html}'

    if tag.name == 'br':
        html += '\n'

    if tag.name == 'span':
        styles = tag.get_attribute_list('style')
        if 'text-decoration: underline;' in styles:
            return f'<u>{html}</u>'

    if tag.name == 'ol' or tag.name == 'ul':
        return '\n'.join(map(lambda row: f'   {row}', html.split('\n')))

    return html


def filter_html(html: str):
    soup = BeautifulSoup(html, 'lxml')
    return filter_tag(soup)


def get_file(file_id):
    bot = telebot.TeleBot(config.TOKEN)
    file = bot.get_file(file_id)
    file_path = file.file_path
    file_url = f'https://api.telegram.org/file/bot{config.TOKEN}/{file_path}'
    response = requests.get(file_url)
    if response.ok:
        return response.content


def get_file_text(file_id):
    bot = telebot.TeleBot(config.TOKEN)
    file = bot.get_file(file_id)
    file_path = file.file_path
    file_url = f'https://api.telegram.org/file/bot{config.TOKEN}/{file_path}'
    response = requests.get(file_url)
    if response.ok:
        return response.text


def make_page_keyboard(has_next_page, call_type):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = []
    page = call_type.page
    page -= 1
    if page >= 1:
        call_type.page = page
        call_data = CallTypes.make_data(call_type)
        prev_page_button = types.InlineKeyboardButton(
            text=f'{Smiles.PREV_PAGE}',
            callback_data=call_data,
        )
        buttons.append(prev_page_button)

    page += 1
    call_type.page = page
    call_data = CallTypes.make_data(CallTypes.Nothing())
    page_number_button = types.InlineKeyboardButton(
        text=f'{call_type.page}',
        callback_data=call_data,
    )
    buttons.append(page_number_button)

    page += 1
    if has_next_page:
        call_type.page = page
        call_data = CallTypes.make_data(call_type)
        next_page_button = types.InlineKeyboardButton(
            text=f'{Smiles.NEXT_PAGE}',
            callback_data=call_data
        )
        buttons.append(next_page_button)

    keyboard.add(*buttons)
    return keyboard
