#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import logging
import os

from telegram.ext import Updater, CommandHandler

from oracles.color import ColorOracle
from oracles.element import ElementOracle
from oracles.number import NumberOracle
from oracles.question import QuestionOracle

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)
token = os.environ['TELEGRAM_TOKEN']


def help(bot, update):
    bot.send_message(update.message.chat_id, text='• Oracolo: concludi la frase con "?".\n  Esempio: Oggi dovrei studiare?\n• Lista: proponimi qualche alternativa separando le scelte con la virgola. Io ti mostrerò la scelta migliore.\n Esempio: cinema, bowling, bar\n• Numeri: "Scegli un numero tra 0 e 25", "Scegli 6 numeri senza ripetizioni da 1 a 90", "Scegli una dozzina di numeri", "Scegli un numero fino a 10"\n• Colore: "Scegli un colore"\n\nNei gruppi ricordati di chiamarmi scrivendo \rm@' + bot.username + ' all\'inizio del messaggio')


def echo(bot, update):
    update.message.text = update.message.text.lower()
    message = update.message.text
    if message.endswith("?"):
        QuestionOracle(bot, update).handle()
    elif update.message.new_chat_member:
        greetings(bot, update)
    elif any(x in message for x in ["scegl", "trov", "estra"]):
        choice(bot, update)
    elif any(x in message for x in [", ", " o ", " oppure "]):
        ElementOracle(bot, update).handle()


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


#####################################
# Choice section
###################################
def choice(bot, update):
    message = update.message.text
    if "numer" in message:
        NumberOracle(bot, update).handle()
    elif "color" in message:
        ColorOracle(bot, update).handle()
    elif any(x in message for x in [",", " o ", " oppure "]):
        ElementOracle(bot, update).handle()


def greetings(bot, update):
    if bot.username in update.message.new_chat_participant.username:
        message = "Salve" + (" a tutti" if update.message.chat.type == "group" else "") + "! Posso essere d'aiuto?"
        bot.send_message(update.message.chat_id, text=message)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("aiuto", help))
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
