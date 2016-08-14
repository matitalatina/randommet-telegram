#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.

"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import re

# Enable logging
from oracles.color import ColorOracle
from oracles.number import NumberOracle

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)
token = os.environ['TELEGRAM_TOKEN']


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='• Oracolo: concludi la frase con "?".\n  Esempio: Oggi dovrei studiare?\n• Lista: proponimi qualche alternativa separando le scelte con la virgola. Io ti mostrerò la scelta migliore.\n Esempio: cinema, bowling, bar\n• Numeri: "Scegli un numero tra 0 e 25", "Scegli 6 numeri senza ripetizioni da 1 a 90", "Scegli una dozzina di numeri", "Scegli un numero fino a 10"\n• Colore: "Scegli un colore"\n\nNei gruppi ricordati di chiamarmi scrivendo \rm@' + bot.username + ' all\'inizio del messaggio')


def echo(bot, update):
    update.message.text = update.message.text.lower()
    message = update.message.text
    if message.endswith("?"):
        oracle(bot, update)
    elif update.message.new_chat_member:
        greetings(bot, update)
    elif any(x in message for x in ["scegl", "trov", "estra"]):
        choice(bot, update)
    elif any(x in message for x in [", ", " o ", " oppure "]):
        choose_elem(bot, update)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


#####################################
# Choice section
###################################
def choice(bot, update):
    message = update.message.text
    if "numer" in message:
        NumberOracle.reply(bot, update)
    elif "color" in message:
        ColorOracle.reply(bot, update)
    elif any(x in message for x in [",", " o ", " oppure "]):
        choose_elem(bot, update)
    #elif "gruppo" in message:
    #    chooseUser(bot, update)


def choose_user(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.chat.first_name)


def choose_elem(bot, update):
    message = update.message.text

    if "@" + bot.username in message:
        string = message.split("@" + bot.username, 1)[1].split(" ", 1)[1]
    else:
        string = message

    items = re.split(", | o | oppure ", string)
    if len(items) > 0:
        items[0] = items[0].split(" ")[-1]
    item_chosen = random.choice(items)
    response = random.choice(["La scelta migliore è ", "Io vi consiglio ", "Sicuramente ", "Non ho dubbi: "]) + item_chosen.strip(" ")
    bot.sendMessage(update.message.chat_id, text=response)


def greetings(bot, update):
    if bot.username in update.message.new_chat_participant.username:
        message = "Salve" + (" a tutti" if update.message.chat.type == "group" else "") + "! Posso essere d'aiuto?"
        bot.sendMessage(update.message.chat_id, text=message)


def oracle(bot, update):
    response = ("Bella domanda " + update.message.from_user.first_name + "... ") if (random.random() <= 0.2) else ""
    response += random.choice(["I segnali indicano sì.",
        "Sì.",
        "Senza dubbio.",
        "Le mie fonti dicono no.",
        "Per come la vedo io, sì.",
        "Puoi contarci.",
        "Concentrati e richiedilo.",
        "Le prospettive non sono così buone.",
        "È decisamente così.",
        "Ora è meglio non dirtelo...",
        "Sono molto dubbioso.",
        "Sì, decisamente.",
        "È certo.",
        "Non posso predirlo ora.",
        "Molto probabilmente.",
        "Richiedilo più tardi.",
        "La mia risposta è no.",
        "Le prospettive sono buone.",
        "Non contarci",
        "Sì, a tempo debito.",
        "Le mie fonti dicono no.",
        "Decisamente no.",
        "Sì.",
        "Devi aspettare.",
        "Ho i miei dubbi.",
        "Le prospettive sono così così.",
        "Mi sembra buono!",
        "Chi lo sa?",
        "Mi piace!",
        "Probabilmente.",
        "Stai scherzando?",
        "Fallo!",
        "Non scommetterci.",
        "Dimenticalo."])
    bot.sendMessage(update.message.chat_id, text=response)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    #dp.addTelegramCommandHandler("start", start)
    dp.add_handler(CommandHandler("aiuto", help))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler([Filters.text], echo))
    dp.add_handler(CommandHandler("rm", echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
