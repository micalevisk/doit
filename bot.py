# -*- coding: utf-8 -*-
import os
import atexit

import botan
import config
import telebot
import i18n

from apscheduler.scheduler import Scheduler
from flask import Flask, request
from pymongo import MongoClient
from telebot import types

from helper import gen_markup, tasks_kb
from lang import btns

server = Flask(__name__)

cron = Scheduler(daemon=True)
cron.start()

bot = telebot.TeleBot(config.token)
botan_key = config.botan_key
client = MongoClient(config.base)
db = client["todo"]

isWrite = False
i18n.load_path.append("lang/")

langs = {"Русский \U0001f1f7\U0001f1fa": "ru", "English \U0001f1fa\U0001f1f8": "en"}
b = []
lang_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
[b.append(l) for l in langs.keys()]
lang_markup.row(b[0], b[1])


@bot.message_handler(commands=["start"])
def start(msg):
    find = db.users.find_one({"id": str(msg.chat.id)})
    if find:
        i18n.set("locale", find["lang"])
        if find["notify"]:
            markup = gen_markup(i18n.t("msg.add"), i18n.t("msg.tasks"), i18n.t("msg.help"), i18n.t("msg.rate"), i18n.t("msg.offn"), i18n.t("msg.setl"))
        else:
            markup = gen_markup(i18n.t("msg.add"), i18n.t("msg.tasks"), i18n.t("msg.help"), i18n.t("msg.rate"), i18n.t("msg.onn"), i18n.t("msg.setl"))
        bot.send_message(msg.chat.id, i18n.t("msg.hi_back"), reply_markup=markup)
        botan.track(botan_key, msg.chat.id, msg, 'Returned user')
        return
    else:
        markup = gen_markup(i18n.t("msg.add"), i18n.t("msg.tasks"), i18n.t("msg.help"), i18n.t("msg.rate"), i18n.t("msg.offn"), i18n.t("msg.setl"))
        db.users.save({"id": str(msg.chat.id), "tasks": [], "notify": True, "lang": "en"})
        bot.send_message(msg.chat.id, i18n.t("msg.hi"),reply_markup=markup)
        botan.track(botan_key, msg.chat.id, msg, 'New user')
        return


@bot.message_handler(commands=["add"])
def add(msg):
    global isWrite
    isWrite = True
    find = db.users.find_one({"id": str(msg.chat.id)})
    i18n.set("locale", find["lang"])

    m = msg.text.replace("/add", "")
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(i18n.t("msg.cancel"))
    if m == "":
        bot.send_message(msg.chat.id, i18n.t("msg.enter"), reply_markup=markup)
    else:
        save_task(msg, msg.chat.id, m)


@bot.message_handler(func=lambda msg: msg.text in btns.add)
def add_task(msg):
    global isWrite
    isWrite = True
    find = db.users.find_one({"id": str(msg.chat.id)})
    i18n.set("locale", find["lang"])

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(i18n.t("msg.cancel"))
    bot.send_message(msg.chat.id, i18n.t("msg.enter"), reply_markup=markup)


@bot.message_handler(commands=["tasks"])
@bot.message_handler(func=lambda msg: msg.text in btns.task)
def my_task(msg):
    global isWrite
    isWrite = False
    find = db.users.find_one({"id": str(msg.chat.id)})
    i18n.set("locale", find["lang"])

    if len(find["tasks"]) != 0:
        bot.send_message(msg.chat.id, i18n.t("msg.taskhelp"), reply_markup=tasks_kb(find["tasks"]))
    else:
        bot.send_message(msg.chat.id, i18n.t("msg.notask"))
    botan.track(botan_key, msg.chat.id, msg, 'Task list')
    return


@bot.message_handler(func=lambda msg: msg.text in btns.cancel)
def cancel(msg):
    global isWrite
    isWrite = False
    find = db.users.find_one({"id": str(msg.chat.id)})
    i18n.set("locale", find["lang"])

    if find["notify"]:
        markup = gen_markup(i18n.t("msg.add"), i18n.t("msg.tasks"), i18n.t("msg.help"), i18n.t("msg.rate"), i18n.t("msg.offn"), i18n.t("msg.setl"))
    else:
        markup = gen_markup(i18n.t("msg.add"), i18n.t("msg.tasks"), i18n.t("msg.help"), i18n.t("msg.rate"), i18n.t("msg.onn"), i18n.t("msg.setl"))

    bot.send_message(msg.chat.id, i18n.t("msg.menu"), reply_markup=markup)


@bot.message_handler(commands=["rate"])
@bot.message_handler(func=lambda msg: msg.text in btns.rate)
def rate(msg):
    find = db.users.find_one({"id": str(msg.chat.id)})
    i18n.set("locale", find["lang"])

    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(
        text=i18n.t("msg.rate"), url="https://t.me/storebot?start=jditbot")
    kb.add(btn)
    bot.send_message(msg.chat.id, i18n.t("msg.thanks"), reply_markup=kb)
    botan.track(botan_key, msg.chat.id, msg, 'Rate')
    return


@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda msg: msg.text in btns.help)
def help(msg):
    find = db.users.find_one({"id": str(msg.chat.id)})
    i18n.set("locale", find["lang"])

    bot.send_message(msg.chat.id, i18n.t("msg.helpme"))
    botan.track(botan_key, msg.chat.id, msg, 'Help')
    return


@bot.message_handler(commands=["lang"])
@bot.message_handler(func=lambda msg: msg.text in btns.setl)
def lang(msg):
    find = db.users.find_one({"id": str(msg.chat.id)})
    i18n.set("locale", find["lang"])
    bot.send_message(msg.chat.id, i18n.t("msg.setlang"), reply_markup=lang_markup)


@bot.message_handler(func=lambda msg: msg.text in btns.off or msg.text in btns.on)
def notifyset(msg):
    find = db.users.find_one({"id": str(msg.chat.id)})
    i18n.set("locale", find["lang"])

    if find["notify"]:
        markup = gen_markup(i18n.t("msg.add"), i18n.t("msg.tasks"), i18n.t("msg.help"), i18n.t("msg.rate"), i18n.t("msg.onn"), i18n.t("msg.setl"))
        db.users.update({"id": str(msg.chat.id)}, {"$set": {"notify": False}})
        bot.send_message(msg.chat.id, i18n.t("msg.disabled"), reply_markup=markup)
    else:
        markup = gen_markup(i18n.t("msg.add"), i18n.t("msg.tasks"), i18n.t("msg.help"), i18n.t("msg.rate"), i18n.t("msg.offn"), i18n.t("msg.setl"))
        db.users.update({"id": str(msg.chat.id)}, {"$set": {"notify": True}})
        bot.send_message(msg.chat.id, i18n.t("msg.enabled"), reply_markup=markup)


@bot.message_handler(func=lambda msg: True)
def msg_hand(msg):
    global isWrite
    if isWrite and msg.text not in langs:
        save_task(msg, msg.chat.id, msg.text)
    elif msg.text in langs:
        find = db.users.find_one({"id": str(msg.chat.id)})
        db.users.update({"id": str(msg.chat.id)}, {"$set": {"lang": langs.get(msg.text)}})
        i18n.set("locale", langs.get(msg.text))
        bot.send_message(msg.chat.id, i18n.t("msg.newlang"))
    isWrite = False


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    find = db.users.find_one({"id": str(call.message.chat.id)})
    i18n.set("locale", find["lang"])

    db.users.update({"id": str(call.message.chat.id)}, {"$pull": {"tasks": find["tasks"][int(call.data)]}}, upsert=False)
    bot.answer_callback_query(call.id, text=i18n.t("msg.completed"))

    find = db.users.find_one({"id": str(call.message.chat.id)})
    if len(find["tasks"]) != 0:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=i18n.t("msg.taskhelp"), reply_markup=tasks_kb(find["tasks"]))
        botan.track(botan_key, call.message.chat.id, call.message, 'Delete task')
        return
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=i18n.t("msg.notask"))


def save_task(msg, cid, text):
    global isWrite
    find = db.users.find_one({"id": str(cid)})
    i18n.set("locale", find["lang"])

    if find["notify"]:
        markup = gen_markup(i18n.t("msg.add"), i18n.t("msg.tasks"), i18n.t("msg.help"), i18n.t("msg.rate"), i18n.t("msg.offn"), i18n.t("msg.setl"))
    else:
        markup = gen_markup(i18n.t("msg.add"), i18n.t("msg.tasks"), i18n.t("msg.help"), i18n.t("msg.rate"), i18n.t("msg.onn"), i18n.t("msg.setl"))

    if len(text) < 50:
        if text not in find["tasks"]:
            db.users.update({"id": str(cid)}, {"$push": {"tasks": text}}, upsert=False)
            bot.send_message(cid, i18n.t("msg.added"), reply_markup=markup)
            botan.track(botan_key, cid, msg, 'Add task')
            return
        else:
            bot.send_message(cid, i18n.t("msg.inlist"), reply_markup=markup)
    else:
        bot.send_message(cid, i18n.t("msg.long"), reply_markup=markup)
    isWrite = False


@cron.interval_schedule(hours=12)
def notify():
    for user in db.users.find():
        if user["tasks"] != [] and user["notify"]:
            i18n.set("locale", user["lang"])
            bot.send_message(user["id"], i18n.t("msg.notify"))


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


server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
server = Flask(__name__)
