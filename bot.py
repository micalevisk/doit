# -*- coding: utf-8 -*-
import atexit
import os

import botan
import config
import telebot

from apscheduler.scheduler import Scheduler
from flask import Flask, request
from helper import get_lang, gen_markup, tasks_kb
from pymongo import MongoClient
from telebot import types

from mymsg import messages

server = Flask(__name__)

cron = Scheduler(daemon=True)
cron.start()

bot = telebot.TeleBot(config.token)
botan_key = config.botan_key
client = MongoClient(config.base)
db = client["todo"]

isWrite = False
kb_hider = types.ReplyKeyboardRemove()


@bot.message_handler(commands=["start"])
def start(msg):
    find = db.users.find_one({"id": str(msg.chat.id)})
    lc = msg.from_user.language_code
    markup = gen_markup(messages.get(get_lang(lc)).get("add"),
                        messages.get(get_lang(lc)).get("mytask"), messages.get(get_lang(lc)).get("help"),
                        messages.get(get_lang(lc)).get("rate"))
    if find:
        bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("welcome"),
                         reply_markup=markup)
        botan.track(botan_key, msg.chat.id, msg, 'Returned user')
        return
    else:
        db.users.save({"id": str(msg.chat.id), "tasks": [], "lang": lc})
        bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("newuser"),
                         reply_markup=markup)
        botan.track(botan_key, msg.chat.id, msg, 'New user')
        return


@bot.message_handler(
    func=lambda msg: msg.text == messages.get(get_lang(msg.from_user.language_code)).get("add"))
def add_task(msg):
    global isWrite
    isWrite = True
    lc = msg.from_user.language_code
    bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("wtask"), reply_markup=kb_hider)


@bot.message_handler(
    func=lambda msg: msg.text == messages.get(get_lang(msg.from_user.language_code)).get("mytask"))
def my_task(msg):
    global isWrite
    isWrite = False

    lc = msg.from_user.language_code
    find = db.users.find_one({"id": str(msg.chat.id)})
    find["tasks"].reverse()
    if len(find["tasks"]) != 0:
        bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("utask"), reply_markup=tasks_kb(find["tasks"]))
    else:
        bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("notask"))
    botan.track(botan_key, msg.chat.id, msg, 'Task list')
    return


@bot.message_handler(
    func=lambda msg: msg.text == messages.get(get_lang(msg.from_user.language_code)).get("back"))
def back(msg):
    global isWrite
    isWrite = False
    lc = msg.from_user.language_code
    markup = gen_markup(messages.get(get_lang(lc)).get("add"), messages.get(get_lang(lc)).get("mytask"),
                        messages.get(get_lang(lc)).get("help"), messages.get(get_lang(lc)).get("rate"))
    bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("menu"), reply_markup=markup)


@bot.message_handler(commands=['rate'])
@bot.message_handler(
    func=lambda msg: msg.text == messages.get(get_lang(msg.from_user.language_code)).get("rate"))
def rate(msg):
    lc = msg.from_user.language_code
    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(
        text=messages.get(get_lang(lc)).get("rate"), url="https://telegram.me/storebot?start=todobobot")
    kb.add(btn)
    bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("textrate"), reply_markup=kb)
    botan.track(botan_key, msg.chat.id, msg, 'Rate')
    return


@bot.message_handler(commands=["help"])
@bot.message_handler(
    func=lambda msg: msg.text == messages.get(get_lang(msg.from_user.language_code)).get("help"))
def help(msg):
    lc = msg.from_user.language_code
    bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("ref"))
    botan.track(botan_key, msg.chat.id, msg, 'Help')
    return


@bot.message_handler(func=lambda msg: True)
def msg_hand(msg):
    global isWrite
    lc = msg.from_user.language_code
    markup = gen_markup(messages.get(get_lang(lc)).get("add"), messages.get(get_lang(lc)).get("mytask"),
                        messages.get(get_lang(lc)).get("help"), messages.get(get_lang(lc)).get("rate"))
    if isWrite:
        find = db.users.find_one({"id": str(msg.chat.id)})
        if len(msg.text) < 50:
            if msg.text not in find["tasks"]:
                isWrite = False
                db.users.update({"id": str(msg.chat.id)}, {"$push": {"tasks": msg.text}}, upsert=False)
                bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("uadd"), reply_markup=markup)
                botan.track(botan_key, msg.chat.id, msg, 'Add task')
                return
            else:
                isWrite = False
                bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("ftask"), reply_markup=markup)
        else:
            isWrite = False
            bot.send_message(msg.chat.id, messages.get(get_lang(lc)).get("maxlen"), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        lc = call.message.from_user.language_code
        find = db.users.find_one({"id": str(call.message.chat.id)})
        db.users.update({"id": str(call.message.chat.id)}, {"$pull": {"tasks": find["tasks"][int(call.data)]}},
                        upsert=False)
        bot.answer_callback_query(call.id, text=messages.get(get_lang(lc)).get("del"))

        find = db.users.find_one({"id": str(call.message.chat.id)})
        find["tasks"].reverse()

        if len(find["tasks"]) != 0:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=messages.get(get_lang(lc)).get("utask"), reply_markup=tasks_kb(find["tasks"]))
            botan.track(botan_key, call.message.chat.id, call.message, 'Delete task')
            return
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=messages.get(get_lang(lc)).get("notask"))


@cron.interval_schedule(hours=12)
def notify():
    for user in db.users.find():
        if user["tasks"] != []:
            bot.send_message(user["id"], messages.get(get_lang(user["lang"])).get("notify"))


atexit.register(lambda: cron.shutdown(wait=False))


@server.route("/bot", methods=["POST"])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=config.url)
    return "ok", 200


server.run(host="0.0.0.0", port=os.environ.get("PORT", 5000))
server = Flask(__name__)
