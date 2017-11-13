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


def gen_markup(add_task, my_task, my_help):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(add_task, my_task)
    markup.row(my_help)
    return markup
