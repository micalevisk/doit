# -*- coding: utf-8 -*-
import os
import atexit

import botan
import config
import telebot

from apscheduler.scheduler import Scheduler
from flask import Flask, request
from pymongo import MongoClient
from telebot import types

from helper import gen_markup, tasks_kb

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
    if find:
        if find["notify"]:
            markup = gen_markup("Add task✏️", "My tasks📝", "Help📚", "Rate⭐️", "Off notifications 🔕")
        else:
            markup = gen_markup("Add task✏️", "My tasks📝", "Help📚", "Rate⭐️", "On notifications 🔔")
        bot.send_message(msg.chat.id, "Welcome back 🎉", reply_markup=markup)
        botan.track(botan_key, msg.chat.id, msg, 'Returned user')
        return
    else:
        markup = gen_markup("Add task✏️", "My tasks📝", "Help📚", "Rate⭐️", "Off notifications 🔕")
        db.users.save({"id": str(msg.chat.id), "tasks": [], "notify": True})
        bot.send_message(msg.chat.id, "Welcome!\nPress button 'Add task ✏️', to create new task 📋",reply_markup=markup)
        botan.track(botan_key, msg.chat.id, msg, 'New user')
        return


@bot.message_handler(commands=["add"])
def add(msg):
    global isWrite
    isWrite = True
    lc = msg.from_user.language_code
    m = msg.text.replace("/add", "")
    if m == "":
        bot.send_message(msg.chat.id, "Enter your task:", reply_markup=kb_hider)
    else:
        save_task(msg, msg.chat.id, m)


@bot.message_handler(func=lambda msg: msg.text == "Add task✏️")
def add_task(msg):
    global isWrite
    isWrite = True
    lc = msg.from_user.language_code
    bot.send_message(msg.chat.id, "Click \"← back\" to cancel\n\nEnter your task:", reply_markup=kb_hider)


@bot.message_handler(commands=["tasks"])
@bot.message_handler(func=lambda msg: msg.text == "My tasks📝")
def my_task(msg):
    global isWrite
    isWrite = False

    lc = msg.from_user.language_code
    find = db.users.find_one({"id": str(msg.chat.id)})
    if len(find["tasks"]) != 0:
        bot.send_message(msg.chat.id, "Press the task in the list in order to finish it 🌝", reply_markup=tasks_kb(find["tasks"]))
    else:
        bot.send_message(msg.chat.id, "You have no tasks❗️")
    botan.track(botan_key, msg.chat.id, msg, 'Task list')
    return


@bot.message_handler(func=lambda msg: msg.text == "← back")
def back(msg):
    global isWrite
    isWrite = False
    find = db.users.find_one({"id": str(msg.chat.id)})
    if find["notify"]:
        markup = gen_markup("Add task✏️", "My tasks📝", "Help📚", "Rate⭐️", "Off notifications 🔕")
    else:
        markup = gen_markup("Add task✏️", "My tasks📝", "Help📚", "Rate⭐️", "On notifications 🔔")

    bot.send_message(msg.chat.id, "Select menu item 🌚", reply_markup=markup)


@bot.message_handler(commands=["rate"])
@bot.message_handler(func=lambda msg: msg.text == "Rate⭐️")
def rate(msg):
    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(
        text="Rate⭐️", url="https://t.me/storebot?start=ne_robot")
    kb.add(btn)
    bot.send_message(msg.chat.id, "Thanks for using ToDo 🚀\nPlease rate it in the StoreBot", reply_markup=kb)
    botan.track(botan_key, msg.chat.id, msg, 'Rate')
    return


@bot.message_handler(commands=["help"])
@bot.message_handler(func=lambda msg: msg.text == "Help📚")
def help(msg):
    bot.send_message(msg.chat.id, "If you have any questions or suggestions, please contact me @enotcode\n\nToDo 🚀 — is a open-source project\nhttps://github.com/enotcode/todobot")
    botan.track(botan_key, msg.chat.id, msg, 'Help')
    return


@bot.message_handler(func=lambda msg: msg.text == "Off notifications 🔕" or msg.text == "On notifications 🔔")
def notifyset(msg):
    find = db.users.find_one({"id": str(msg.chat.id)})
    if find["notify"]:
        markup = gen_markup("Add task✏️", "My tasks📝", "Help📚", "Rate⭐️", "On notifications 🔔")
        db.users.update({"id": str(msg.chat.id)}, {"$set": {"notify": False}})
        bot.send_message(msg.chat.id, "Notifications are disabled 🔕", reply_markup=markup)
    else:
        markup = gen_markup("Add task✏️", "My tasks📝", "Help📚", "Rate⭐️", "Off notifications 🔕")
        db.users.update({"id": str(msg.chat.id)}, {"$set": {"notify": True}})
        bot.send_message(msg.chat.id, "Notifications are enabled 🔔", reply_markup=markup)


@bot.message_handler(func=lambda msg: True)
def msg_hand(msg):
    global isWrite
    if isWrite:
        save_task(msg, msg.chat.id, msg.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    find = db.users.find_one({"id": str(call.message.chat.id)})
    db.users.update({"id": str(call.message.chat.id)}, {"$pull": {"tasks": find["tasks"][int(call.data)]}}, upsert=False)
    bot.answer_callback_query(call.id, text="The task was completed ✔️")

    find = db.users.find_one({"id": str(call.message.chat.id)})
    if len(find["tasks"]) != 0:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Press the task in the list in order to finish it 🌝", reply_markup=tasks_kb(find["tasks"]))
        botan.track(botan_key, call.message.chat.id, call.message, 'Delete task')
        return
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="You have not tasks❗️")


def save_task(msg, cid, text):
    global isWrite
    find = db.users.find_one({"id": str(cid)})
    if find["notify"]:
        markup = gen_markup("Add task✏️", "My tasks📝", "Help📚", "Rate⭐️", "Off notifications 🔕")
    else:
        markup = gen_markup("Add task✏️", "My tasks📝", "Help📚", "Rate⭐️", "On notifications 🔔")

    if len(text) < 50:
        if text not in find["tasks"]:
            db.users.update({"id": str(cid)}, {"$push": {"tasks": text}}, upsert=False)
            bot.send_message(cid, "Your task was added ✅", reply_markup=markup)
            botan.track(botan_key, cid, msg, 'Add task')
            return
        else:
            bot.send_message(cid, "This task is already in the list❗️", reply_markup=markup)
    else:
        bot.send_message(cid, "The task is too long❗️", reply_markup=markup)
    isWrite = False


@cron.interval_schedule(hours=12)
def notify():
    for user in db.users.find():
        if user["tasks"] != [] and user["notify"]:
            bot.send_message(user["id"], "You have uncompleted tasks 😥")


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
