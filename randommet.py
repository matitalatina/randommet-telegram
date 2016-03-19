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

from telegram import Updater
import logging
import random
import re

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='• Oracolo: concludi la frase con "?".\n  Esempio: Oggi dovrei studiare?\n• Lista: proponimi qualche alternativa separando le scelte con la virgola. Io ti mostrerò la scelta migliore.\n Esempio: cinema, bowling, bar\n• Numeri: "Scegli un numero tra 0 e 25", "Scegli 6 numeri senza ripetizioni da 1 a 90", "Scegli una dozzina di numeri", "Scegli un numero fino a 10"\n• Colore: "Scegli un colore"\n\nNei gruppi ricordati di chiamarmi scrivendo @' + bot.username + ' all\'inizio del messaggio')


def echo(bot, update):
    update.message.text = update.message.text.lower()
    message = update.message.text
    if message.endswith("?"):
        oracle(bot, update)
    elif update.message.new_chat_participant:
        greetings(bot, update)
    elif any(x in message for x in ["scegl", "trov", "estra"]):
        choice(bot, update)
    elif any(x in message for x in [", ", " o ", " oppure "]):
        chooseElem(bot, update)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

#####################################
# Choice section
###################################
def choice(bot, update):
    message = update.message.text
    if "numer" in message:
        chooseNumber(bot, update)
    elif "color" in message:
        chooseColor(bot, update)
    elif any(x in message for x in [",", " o ", " oppure "]):
        chooseElem(bot, update)


def chooseNumber(bot, update):
    message = update.message.text
    messageWoStringNumbers = replaceTextNumbers(message)
    numbers = extractNumbersFromString(messageWoStringNumbers)
    lenNumber = len(numbers)

    if lenNumber == 1:
        showNumbers(bot, update, [random.randrange(numbers[0])])
    elif lenNumber == 2:
        showNumbers(bot, update, [random.randrange(min(numbers), max(numbers))])
    elif lenNumber > 2:
        chooseRangeNumbers(bot, update, numbers)
    else:
        showNumbers(bot, update, [random.randrange(101)])

def chooseColor(bot, update):
    colors = getColors()
    colorName = random.choice(list(colors.keys()))
    hexVal = colors[colorName]
    dummyImageUrl = "http://dummyimage.com/300/{0}/{0}".format(hexVal)
    response = random.choice(["Per me ti andrebbe bene questo: ", "La scelta migliore è: "]) + colorName + "\n" + dummyImageUrl
    bot.sendMessage(update.message.chat_id, text=response)

def chooseRangeNumbers(bot, update, numbers):
    message = update.message.text
    chosenNumbers = [0]
    numberElems, *rangeNumber = numbers

    if any(x in message for x in [" senza ripet"]):
        chosenNumbers = random.sample(range(min(rangeNumber), max(rangeNumber) + 1), numberElems)
    else:
        chosenNumbers = [random.randrange(min(rangeNumber), max(rangeNumber) + 1) for p in range(numberElems)]

    showNumbers(bot, update, chosenNumbers)

def showNumbers(bot, update, numbers):
    response = "Ecco qui: " + ", ".join(map(str, numbers))
    bot.sendMessage(update.message.chat_id, text=response)


def extractNumbersFromString(text):
    return [int(s) for s in text.split() if s.isdigit()]

def replaceTextNumbers(text):
    rep = textNumbers()

    # use these three lines to do the replacement
    rep = dict((re.escape(k), str(v)) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    return text

def textNumbers():
    return {
        'uno': 1,
        'due': 2,
        'coppia': 2,
        'tre': 3,
        'tripletta': 3,
        'quattro': 4,
        'cinque': 5,
        'sei': 6,
        'sette': 7,
        'otto': 8,
        'nove': 9,
        'dieci': 10,
        'undici': 11,
        'dodici': 12,
        'dozzina': 12,
        'tredici': 13
    }

def chooseElem(bot, update):
    message = update.message.text

    if "@" + bot.username in message:
        string = message.split("@" + bot.username, 1)[1].split(" ", 1)[1]
    else:
        string = message

    items = re.split(", | o | oppure ", string)
    if len(items) > 0:
        items[0] = items[0].split(" ")[-1]
    itemChosen = random.choice(items)
    response = random.choice(["La scelta migliore è ", "Io vi consiglio ", "Sicuramente ", "Non ho dubbi: "]) + itemChosen.strip(" ")
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


def getColors():
    return {"Albicocca": "fbceb1",
    "Amaranto": "E52B50",
    "Ambra": "FFBF00",
    "Ametista": "884DA7",
    "Anguria": "fc6c85",
    "Antracite": "293133",
    "Aragosta": "ed7465",
    "Arancione": "FFA500",
    "Ardesia": "708090",
    "Argento": "C0C0C0",
    "Asparago": "87a96b",
    "Avio": "5D8AA8",
    "Avorio": "FFFFF0",
    "Azalea": "d3305d",
    "Azzurro": "007fff",
    "Azzurro fiordaliso": "ABCDEF",
    "Beige": "f5f5dc",
    "Beige-oliva chiaro": "908435",
    "Beige verdastro": "BEBD7F",
    "Bianco": "FFFFFF",
    "Bianco antico": "FFFEEF",
    "Bianco anti-flash": "F2F3F4",
    "Bianco di titanio": "FAEBD7",
    "Bianco di zinco": "FEFEE9",
    "Bianco fantasma": "F8F8FF",
    "Bianco floreale": "FFFAF0",
    "Bianco fumo": "F5F5F5",
    "Bianco Navajo": "FFDEAD",
    "Biscotto": "FFE4C4",
    "Bistro": "3D2B1F",
    "Blu": "0000ff",
    "Blu acciaio": "4682B4",
    "Blu alice": "F0F8FF",
    "Blu Bondi": "0095B6",
    "Blu cadetto": "5F9EA0",
    "Blu ceruleo": "2A52BE",
    "Blu comando stellare": "007BB8",
    "Blu di Persia": "1C39BB",
    "Blu di Prussia": "003153",
    "Blu Dodger": "1e90ff",
    "Blu elettrico": "003399",
    "Blu Klein": "002FA7",
    "Blu marino": "000080",
    "Blu notte": "343A90",
    "Blu oltremare": "120A8F",
    "Blu reale": "4169E1",
    "Bordeaux": "800000",
    "Borgogna": "800020",
    "Bronzo": "CD7F32",
    "Bronzo antico": "75663F",
    "Camoscio": "F0DC82",
    "Carbone": "050402",
    "Cardo": "D8BFD8",
    "Carminio": "960018",
    "Carta da zucchero": "e0ffff",
    "Castagno": "CD5C5C",
    "Castagno scuro": "986960",
    "Castano chiaro": "DDADAF",
    "Catrame": "D2B48C",
    "Catrame scuro": "918151",
    "Celadon": "ACE1AF",
    "Celeste": "99CBFF",
    "Ceruleo": "007BA7",
    "Ceruleo scuro": "08457E",
    "Chartreuse": "7fff00",
    "Ciano": "00ffff",
    "Ciliegia": "DE3163",
    "Cioccolato": "D2691E",
    "Cobalto": "0047AB",
    "Conchiglia": "FFF5EE",
    "Corallo": "ff7f50",
    "Crema": "FFFDD0",
    "Cremisi": "dc143c",
    "Denim": "1560BD",
    "Denim chiaro": "5E86C1",
    "Eliotropo": "DF73FF",
    "Ecru": "C2B280",
    "Fiore di granturco": "6495ED",
    "Foglia di tè": "008080",
    "Fucsia": "f400a1",
    "Fucsia Bordesto Lillato": "E0AFEE",
    "Fulvo": "EBB55F",
    "Gainsboro": "DCDCDC",
    "Giada": "00A86B",
    "Giallo": "ffff00",
    "Giallo miele": "A98307",
    "Giallo Napoli": "F7E89F",
    "Giallo pastello": "FFFF66",
    "Giallo sabbia": "C6A664",
    "Giallo segnale": "E5BE01",
    "Giallo scuolabus": "ffd800",
    "Glicine": "C9A0DC",
    "Granata": "7B1B02",
    "Grano": "F5DEB3",
    "Grigio": "808080",
    "Grigio 5%": "F7F7F7",
    "Grigio 10%": "EFEFEF",
    "Grigio 20%": "D2D2D2",
    "Grigio 30%": "B2B2B2",
    "Grigio 40%": "8F8F8F",
    "Grigio 50%": "808080",
    "Grigio 60%": "5F5F5F",
    "Grigio 70%": "4F4F4F",
    "Grigio 75%": "404040",
    "Grigio 80%": "2F2F2F",
    "Grigio asparago": "465945",
    "Grigio ardesia scuro": "2F4F4F",
    "Grigio ardesia chiaro": "778899",
    "Grigio cenere": "E4E5E0",
    "Grigio rosso chiaro": "D0AFAE",
    "Grigio tè verde": "CADABA",
    "Grigio topo": "646B63",
    "Incarnato prugna": "CC8899",
    "Indaco": "4B0082",
    "Indaco elettrico": "6F00FF",
    "Indaco scuro": "310062",
    "International Klein Blue": "002FA7",
    "Isabella": "F4F0EC",
    "Kaki": "C3B091",
    "Kaki chiaro": "F0E68C",
    "Kaki scuro": "BDB76B",
    "Lampone": "E30B5C",
    "Lavanda": "E6E6FA",
    "Lavanda pallido": "DABAD0",
    "Lavanda rosata": "FFF0F5",
    "Limone": "FDE910",
    "Limone crema": "FFFACD",
    "Lilla": "C8A2C8",
    "Lime": "CCFF00",
    "Lino": "FAF0E6",
    "Magenta": "FF00FF",
    "Magenta chiaro": "F984E5",
    "Magnolia": "F8F4FF",
    "Malva": "993366",
    "Malva chiaro": "996666",
    "Mandarino": "FFCC00",
    "Marrone": "964B00",
    "Marrone chiaro": "CD853F",
    "Marrone pastello": "987654",
    "Marrone-rosso": "993300",
    "Marrone sabbia chiaro": "DABDAB",
    "Marrone scuro": "654321",
    "Melanzana": "990066",
    "Mogano": "C04000",
    "Nero": "000000",
    "Ocra": "CC7722",
    "Olivina": "9AB973",
    "Orchidea": "DA70D6",
    "Oro": "ffd700",
    "Oro vecchio": "CFB53B",
    "Ottone antico": "CC9966",
    "Papaia": "FFEFD5",
    "Pera": "D1E231",
    "Pervinca": "CCCCFF",
    "Pesca": "FFE5B4",
    "Pesca scuro": "FFDAB9",
    "Pesca-arancio": "FFCC99",
    "Pesca-giallo": "FADFAD",
    "Pistacchio": "93C572",
    "Platino": "E5E4E2",
    "Porpora": "B20000",
    "Prugna": "660066",
    "Rame": "b87333",
    "Registration black": "000000",
    "Rosa": "FFC0CB",
    "Rosa arancio": "FF9966",
    "Rosa medio": "DB244F",
    "Rosa Mountbatten": "997A8D",
    "Rosa pallido": "FADADD",
    "Rosa pastello": "FFD1DC",
    "Rosa scuro": "E75480",
    "Rosa shocking": "FC0FC0",
    "Rosa vivo": "FF007F",
    "Rosso": "FF0000",
    "Rosso aragosta": "cc5500",
    "Rosso cardinale": "C41E3A",
    "Rosso corsa": "CC0000",
    "Rosso Falun": "801818",
    "Rosso fragola": "CE3018",
    "Rosso fuoco": "A61022",
    "Rosso mattone": "C41E3A",
    "Rosso mattone chiaro": "BD8E80",
    "Rosso pomodoro": "FF6347",
    "Rosso pompeiano": "D21F1B",
    "Rosso rosa": "FF6088",
    "Rosso sangue": "500000",
    "Rosso segnale": "A52019",
    "Rosso Tiziano": "BA6262",
    "Rosso veneziano": "C80815",
    "Rosso violaceo": "C71585",
    "Rosso violetto chiaro": "DB7093",
    "Rubino": "410012",
    "Sabbia": "F4A460",
    "Salmone": "FF8C69",
    "Salmone scuro": "E9967A",
    "Sangria": "92000A",
    "Scarlatto": "FF2400",
    "Scarlatto scuro": "560319",
    "Seppia": "704214",
    "Solidago": "DAA520",
    "Solidago scuro": "B8860B",
    "Tan": "D2B48C",
    "Tenné": "CD5700",
    "Terra d’ombra": "635147",
    "Terra d’ombra bruciata": "8A3324",
    "Terra di Siena": "E97451",
    "Terra di Siena bruciata": "531B00",
    "Testa di moro": "754909",
    "Tè verde": "D0F0C0",
    "Tè verde scuro": "BADBAD",
    "Tronco": "79443B",
    "Turchese": "30D5C8",
    "Turchese chiaro": "08E8DE",
    "Turchese pallido": "99FFCC",
    "Turchese scuro": "116062",
    "Turchese Perla Mistica": "99FFCC",
    "Uovo di pettirosso": "00CCCC",
    "Uovo di pettirosso chiaro": "96DED1",
    "Verde": "00ff00",
    "Verde Caraibi": "00CC99",
    "Verde foresta": "228b22",
    "Verde chiaro": "66FF00",
    "Verde-giallo": "ADFF2F",
    "Verde marino": "2E8B57",
    "Verde marino medio": "3CB371",
    "Verde marino scuro": "8FBC8F",
    "Verde menta": "98FF98",
    "Verde menta chiaro": "A6FBB2",
    "Verde muschio": "ADDFAD",
    "Verde oliva": "808000",
    "Verde olivastro": "6B8E23",
    "Verde oliva scuro": "556B2F",
    "Verde pastello": "77DD77",
    "Verde pino": "01796F",
    "Verde primavera": "00FF7F",
    "Verde primavera scuro": "177245",
    "Verde ufficio": "008000",
    "Verde smeraldo": "50c878",
    "Verde Veronese": "40826D",
    "Vermiglio": "FF4D00",
    "Viola": "8F00ff",
    "Viola chiaro": "9F00FF",
    "Viola melanzana": "991199",
    "Vinaccia": "C0007F",
    "Zafferano": "F4C430",
    "Zafferano profondo": "FF9933",
    "Zaffiro": "0F52BA"}



def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("***YOUR_TOKEN_HERE***")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    #dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("aiuto", help)

    # on noncommand i.e message - echo the message on Telegram
    dp.addTelegramMessageHandler(echo)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
