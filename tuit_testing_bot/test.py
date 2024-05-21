import json
import config
import random

from app.models import BotUser, Template, Question


def filter_text(text):
    return text.strip()


def filter_(options):
    options_list = options.split('\n')
    options_list = list(map(lambda option: option.strip(), options_list))
    return '\n'.join(options_list)


for question in Question.questions.all():
    options = question.options_uz.split('\n')
    random.shuffle(options)
    question.options_uz = '\n'.join(options)
    options = question.options_ru.split('\n')
    random.shuffle(options)
    question.options_ru = '\n'.join(options)
    question.save()
