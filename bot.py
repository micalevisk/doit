# -*- coding: utf-8 -*-
import telebot

bot = telebot.TeleBot("")


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Welcome 🚀")


if __name__ == '__main__':
    bot.polling(none_stop=True)
