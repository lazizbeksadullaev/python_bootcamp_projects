from telebot import TeleBot, types


TOKEN = '5142087260:AAEZRe6ZUP3Ng9vDiUoIF5PI7zEnJsFd1eQ'

bot = TeleBot(token=TOKEN, parse_mode='HTML')

#o'yin qanday o'lchamda bo'lishini bildiruvchi const
SIZE = 3
#empty=0 consti, o'yinda hali yurilmagan kataklarni bildiradi
EMPTY = 0
#nought=1 bo'lsa demak bu cell(katak, button=1)ga nought yurilganini bildiradi
NOUGHT = 1
#cross=2 bo'lsa demak bu cell(katak, button=2)ga cross yurilganini bildiradi
CROSS = 2

#not_finished=0 consti o'yin hali tugallanmaganligini bildiradi
NOT_FINISHED = 0
#draw=-1 consti o'yin durrang bilab tugaganini bildiradi
DRAW = -1
#nought_win=nought=1 consti noughtlar g'alaba qozonganini bildiradi
NOUGHT_WIN = NOUGHT
#cross_win=cross=2 consti crosslar g'alaba qozonganini bildiradi
CROSS_WIN = CROSS

#o'yinni holatini jadval shaklinda saqlab turuvchi dict
games = dict()


GAME_START_TEXT = "<b>🎮 O'yin boshlandi</b>"
GAME_FINISH_TEXT = "<b>🏁 O'yin tugadi</b>"

MOVE_TEXT = {
    NOUGHT: "<b>⭕️ yurishi</b>",
    CROSS: "<b>❌ yurishi</b>"
}

WIN_TEXT = {
    NOUGHT: "<b>⭕️ yutdi</b>",
    CROSS: "<b>❌ yutdi</b>",
}
DRAW_TEXT = "<b>🤝 Durrang</b>"

RESTART_TEXT = "🔁 Qayta o'ynash"

WRONG_MOVE = "<b>❗️ Xato yurish\n</b><i>⚠️ Qayta yuring</i>"

#SIZExSIZE lik bo'sh buttonlardan iborat table yasash funksiyasi
def create_game_buttons() -> list[list]:
    table = [[EMPTY for _ in range(SIZE)]
             for _ in range(SIZE)]

    return table

# yurilayotgan (i,j) katak bo'sh yoki bo'shmaslikini tekshiruvchi funksiya
def check_move(table, i, j) -> bool:
    return table[i][j] == EMPTY

# tableni berilgan indexdagi qatori hammasi bir xil eltladan tashkil topganlikini va 
# bu qator bo'shmaslikini tekshiruvchi funksiya
def check_row_equal(table, row_index) -> bool:
    row = table[row_index]
    return len(set(row)) == 1 and row[0] != EMPTY

# tableni berilgan indexdagi ustuni hammasi bir xil eltladan tashkil topganlikini va 
# bu ustun bo'shmaslikini tekshiruvchi funksiya
def check_column_equal(table, column_index) -> bool:
    column = [table[i][column_index] for i in range(SIZE)]
    return len(set(column)) == 1 and column[0] != EMPTY

# tableni asosiy dioganali hammasi bir xil eltladan tashkil topganlikini va 
# bu diogonalda bo'sh cellar yo'qlikini tekshiruvchi funksiya
def check_main_diagonal_equal(table):
    column = [table[i][i] for i in range(SIZE)]
    return len(set(column)) == 1 and column[0] != EMPTY

# tableni qo'shimcha dioganali hammasi bir xil eltladan tashkil topganlikini va 
# bu diogonalda bo'sh cellar yo'qlikini tekshiruvchi funksiya
def check_secondary_diagonal_equal(table):
    column = [table[i][-i - 1] for i in range(SIZE)]
    return len(set(column)) == 1 and column[0] != EMPTY

#
def check_game(table):
    for i in range(SIZE):
        if check_row_equal(table, i):
            return table[i][0]
        if check_column_equal(table, i):
            return table[0][i]

    if check_main_diagonal_equal(table):
        return table[0][0]

    if check_secondary_diagonal_equal(table):
        return table[0][-1]

    if moves_count(table) == SIZE*SIZE:
        return DRAW

    return NOT_FINISHED


def set_game_buttons(chat_id, message_id, game_buttons):
    global games
    games[chat_id, message_id] = game_buttons


def move(table, row_index, column_index):
    table[row_index][column_index] = whose_move(table)


def moves_count(table):
    return sum([sum([cell != EMPTY for cell in row]) for row in table])


def whose_move(table):
    moves = moves_count(table)
    return (moves + 0) % 2 + 1


def make_cell_callback_data(i, j):
    return f'{i}x{j}'


def parse_cell_callback_data(data):
    return map(int, data.split('x'))


def check_callback_data_to_cell(data):
    try:
        parse_cell_callback_data(data)
    except Exception:
        return False
    else:
        return True


def make_keyboard_buttons(game_buttons):
    convert = {
        0: '❔',
        1: '⭕️',
        2: '❌',
    }
    buttons = [[EMPTY for _ in range(SIZE)]
               for _ in range(SIZE)]
    for row_index, row in enumerate(game_buttons):
        for column_index, cell in enumerate(row):
            inline_button = types.InlineKeyboardButton(
                text=convert[cell],
                callback_data=make_cell_callback_data(row_index, column_index)
            )
            buttons[row_index][column_index] = inline_button

    return buttons


def make_game_keyboard(chat_id, message_id):
    keyboard = types.InlineKeyboardMarkup(row_width=SIZE)
    game_buttons = games[chat_id, message_id]
    for row in make_keyboard_buttons(game_buttons):
        keyboard.add(*row)

    return keyboard


def make_restart_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text=RESTART_TEXT,
                                        callback_data='restart')
    keyboard.add(button)
    return keyboard


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    bot.send_message(message.chat.id, GAME_START_TEXT)
    chat_id = message.chat.id
    message = bot.send_message(chat_id, GAME_START_TEXT)
    game_buttons = create_game_buttons()
    set_game_buttons(message.chat.id, message.id, game_buttons)
    text = MOVE_TEXT[whose_move(game_buttons)]
    keyboard = make_game_keyboard(message.chat.id, message.id)
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=message.id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: call.data == 'restart')
def restart_callback_query_handler(call):
    game_buttons = create_game_buttons()
    set_game_buttons(call.message.chat.id, call.message.id, game_buttons)
    text = MOVE_TEXT[whose_move(game_buttons)]
    keyboard = make_game_keyboard(call.message.chat.id, call.message.id)
    bot.edit_message_text(
        text=text,
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(
    func=lambda call: check_callback_data_to_cell(call.data),
)
def callback_query_handler(call):
    global games
    row_index, column_index = parse_cell_callback_data(call.data)
    chat_id = call.message.chat.id
    message_id = call.message.id
    table = games[chat_id, message_id]
    if not check_move(table, row_index, column_index):
        text = WRONG_MOVE
        keyboard = make_game_keyboard(chat_id, message_id)
    else:
        move(table, row_index, column_index)
        result = check_game(table)
        if result == DRAW:
            text = DRAW_TEXT
            keyboard = make_restart_keyboard()
        elif result != NOT_FINISHED:
            text = WIN_TEXT[result]
            keyboard = make_restart_keyboard()
        else:
            text = MOVE_TEXT[whose_move(table)]
            keyboard = make_game_keyboard(chat_id, message_id)

    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=keyboard,
    )


bot.polling()
