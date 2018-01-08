from telebot import types

def gen_markup(add_task, my_task, my_help, rate, notify):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(add_task, my_task)
    markup.row(my_help, rate)
    markup.row(notify)
    return markup


def tasks_kb(tasks):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(tasks)):
        button = types.InlineKeyboardButton(text=tasks[i], callback_data=str(i))
        keyboard.add(button)
    return keyboard
