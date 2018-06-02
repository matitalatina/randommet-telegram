from telegram import ParseMode
from telegram.ext import CommandHandler


class HelpCommandHandler(CommandHandler):
    def __init__(self, command):
        super().__init__(command, self.callback)

    @staticmethod
    def callback(bot, update):
        bot.send_message(update.message.chat_id,
                         text=f"""
• **Oracolo**: concludi la frase con "?".\n
  Esempio: *Oggi dovrei studiare?*\n
• **Lista**: proponimi qualche alternativa separando le scelte con la virgola. Io ti mostrerò la scelta migliore.\n
  Esempio: cinema, bowling, bar\n
• **Numeri**: "*Scegli un numero tra 0 e 25*", "*Scegli 6 numeri senza ripetizioni da 1 a 90*", "*Scegli una dozzina di numeri*", "*Scegli un numero fino a 10*"\n
• **Colore**: "*Scegli un colore*"\n
 
Nei gruppi ricordati di chiamarmi scrivendo /rm@{bot.username} all'inizio del messaggio.""",
                         parse_mode=ParseMode.MARKDOWN)
