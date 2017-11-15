from telebot import types


def get_lang(lang_code):
    if not lang_code:
        return "en"
    if "-" in lang_code:
        lang_code = lang_code.split("-")[0]
    if lang_code == "ru":
        return "ru"
    else:
        return "en"


def gen_markup(add_task, my_task, my_help, rate):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(add_task, my_task)
    markup.row(my_help, rate)
    return markup


def tasks_kb(tasks):
    keyboard = types.InlineKeyboardMarkup()
    for i in tasks:
        button = types.InlineKeyboardButton(text=i, callback_data=i)
        keyboard.add(button)
    return keyboard
