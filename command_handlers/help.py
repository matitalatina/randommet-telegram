from telegram import ParseMode
from telegram.ext import CommandHandler


class HelpCommandHandler(CommandHandler):
    def __init__(self, command):
        super().__init__(command, self.callback)

    @staticmethod
    def callback(bot, update):
        bot.send_message(update.message.chat_id,
                         text=f"""
• *Oracolo*: concludi la frase con "?".\n
  Esempio: _Oggi dovrei studiare?_\n
• *Lista*: proponimi qualche alternativa separando le scelte con la virgola. Io ti mostrerò la scelta migliore.\n
  Esempio: cinema, bowling, bar\n
• *Numeri*: "_Scegli un numero tra 0 e 25_", "_Scegli 6 numeri senza ripetizioni da 1 a 90_", "_Scegli una dozzina di numeri_", "_Scegli un numero fino a 10_"\n
• *Colore*: "_Scegli un colore_"\n
 
Nei gruppi ricordati di chiamarmi scrivendo /rm@{bot.username} all'inizio del messaggio.""",
                         parse_mode=ParseMode.MARKDOWN)
