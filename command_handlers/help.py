from telegram import ParseMode
from telegram.ext import CommandHandler


class HelpCommandHandler(CommandHandler):
    def __init__(self, command):
        super().__init__(command, self.callback)

    @staticmethod
    def callback(bot, update):
        bot.send_message(update.message.chat_id,
                         text=f"""
• <b>Oracolo</b>: concludi la frase con "?".\n
  Esempio: <i>Oggi dovrei studiare?</i>\n
• <b>Lista</b>: proponimi qualche alternativa separando le scelte con la virgola. Io ti mostrerò la scelta migliore.\n
  Esempio: cinema, bowling, bar\n
• <b>Numeri</b>: "<i>Scegli un numero tra 0 e 25</i>", "<i>Scegli 6 numeri senza ripetizioni da 1 a 90</i>", "<i>Scegli una dozzina di numeri</i>", "<i>Scegli un numero fino a 10</i>"\n
• <b>Colore</b>: "<i>Scegli un colore</i>"\n
 
Nei gruppi ricordati di chiamarmi scrivendo @{bot.username} all'inizio del messaggio.""",
                         parse_mode=ParseMode.HTML)
