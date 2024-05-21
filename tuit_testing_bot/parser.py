import os
import re
import traceback
import datetime
from zipfile import BadZipFile

from docx import Document

import config
from app.models import Test, Question, TestOne


TESTS_DIR = 'tests'


def filter_row(row):
    new_row = [row[0]]
    for i in range(1, len(row)):
        if row[i] == row[i - 1]:
            continue

        new_row.append(row[i])

    return new_row


def get_title(file_name):
    pattern = "[a-zA-Zа-яА-Я].*[.]"
    result = re.findall(pattern, file_name)[0]
    title = result.removesuffix('.')
    return title


def parse_tests(file_path):
    doc = Document(file_path)
    first = True
    tests = []
    tables = doc.tables
    for table in tables:
        for row in table.rows:
            cells = []
            for cell in row.cells:
                cells.append(cell.text)

            if not any(cells):
                continue

            try:
                cells = filter_row(cells)[-5:]
                question = cells[0]
                answer = cells[1]
                options = cells[1:]
            except Exception:
                traceback.print_exc()
                print(file_path, cells)
            else:
                if first:
                    first = False
                    continue

                tests.append((question, answer, options))

    return tests


id = 1


def create_test(title, tests):
    global id
    test = Test.tests.create(id=id,
                             title=title,
                             duration=datetime.time(0, 40),
                             questions_count=40)
    id += 1
    for number, test_ in enumerate(tests, 1):
        question, answer, options_list = test_
        options_list = list(map(lambda option: option.replace('\n', ' '),
                                options_list))
        options = '\n'.join(options_list)
        question = Question.questions.create(
            type=Question.Type.SINGLE,
            title_uz=question,
            title_ru=question,
            options_uz=options,
            options_ru=options,
            answers_uz=answer,
            answers_ru=answer,
        )
        TestOne.objects.create(test=test,
                               question=question,
                               number=number)


def main():
    for dir in os.listdir(TESTS_DIR):
        file_name = dir
        file_path = os.path.join(TESTS_DIR, file_name)
        if not file_name.endswith('.docx'):
            continue

        try:
            tests = parse_tests(file_path)
            title = get_title(file_name)
            create_test(title, tests)
            print(title)
            # print(tests[0])
        except BadZipFile:
            pass
        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    main()