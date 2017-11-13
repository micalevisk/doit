# -*- coding: utf-8 -*-
import config
import telebot

from telebot import types
from helper import get_lang, gen_markup
from mymsg import messages

bot = telebot.TeleBot(config.token)


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


if __name__ == '__main__':
    bot.polling(none_stop=True)
