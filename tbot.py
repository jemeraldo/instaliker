# coding: utf8
import telegram
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
import re
import evodb

bot = telegram.Bot(token='502243941:AAFbHlkv_7TBAWhhoi1v4Nu0e7q0RRfb6lA')

updater = Updater(token='502243941:AAFbHlkv_7TBAWhhoi1v4Nu0e7q0RRfb6lA')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',\
                    level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hello! send /code <code> to subscribe for statistics')

def register(bot, update):
    result = re.match(r'/code ([0-9A-Z]+$)', update.message.text)
    if len(result.groups()) < 1:
        bot.send_message(chat_id=update.message.chat_id, text=r'Format: /code <code>')
        return None
    code = result.group(1)
    if evodb.set_user_telegram_chat_id(code, update.message.chat_id):
        bot.send_message(chat_id=update.message.chat_id, text='Registered.')
    else:
        bot.send_message(chat_id=update.message.chat_id, text='User has not finded.')

def send_feedback(chat_id, cashierName, rating):
    bot.sendMessage(chat_id, 'Продавец %s только что получил оценку: %s' % (cashierName, rating))

start_handler = CommandHandler('start', start)
register_handler = CommandHandler('code', register)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(register_handler)

updater.start_polling()

