# -*- coding: utf-8 -*-
import telebot

from telebot import types
from mymsg import messages

bot = telebot.TeleBot(<TOKEN>)


@bot.message_handler(commands=["start"])
def start(msg):
    lc = msg.from_user.language_code
    markup = gen_markup(messages.get(get_lang(lc)).get("add"),
                        messages.get(get_lang(lc)).get("mytask"), messages.get(get_lang(lc)).get("help"))
    bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("welcome"),
                     reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text == messages.get(get_lang(msg.from_user.language_code)).get("add").decode('utf-8'))
def add_task(msg):
    lc = msg.from_user.language_code
    bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("wtask"))


@bot.message_handler(func=lambda msg: msg.text == messages.get(get_lang(msg.from_user.language_code)).get("mytask").decode('utf-8'))
def my_task(msg):
    lc = msg.from_user.language_code
    bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("utask"))


@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda msg: msg.text == messages.get(get_lang(msg.from_user.language_code)).get("help").decode('utf-8'))
def help(msg):
    lc = msg.from_user.language_code
    bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("ref"))


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


if __name__ == '__main__':
    bot.polling(none_stop=True)
