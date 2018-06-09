from telegram.ext import MessageHandler

from oracles.color import ColorOracle
from oracles.element import ElementOracle
from oracles.number import NumberOracle
from oracles.place import PlaceOracle
from oracles.question import QuestionOracle


class OracleMessageHandler(MessageHandler):
    def __init__(self):
        super().__init__(None, self.callback)

    @classmethod
    def callback(cls, bot, update):
        update.message.text = cls.sanitize_message(update.message.text, bot.username)
        message = update.message.text
        if message.endswith("?"):
            if message.startswith("dove "):
                return PlaceOracle.from_env(bot, update).handle()
            return QuestionOracle(bot, update).handle()
        elif update.message.new_chat_members:
            return cls.greetings(bot, update)
        elif any(x in message for x in ["scegl", "trov", "estra"]):
            return cls.choice(bot, update)
        elif any(x in message for x in [", ", " o ", " oppure "]):
            return ElementOracle(bot, update).handle()

    @staticmethod
    def choice(bot, update):
        message = update.message.text
        if "numer" in message:
            NumberOracle(bot, update).handle()
        elif "color" in message:
            ColorOracle(bot, update).handle()
        elif any(x in message for x in [",", " o ", " oppure "]):
            ElementOracle(bot, update).handle()

    @staticmethod
    def greetings(bot, update):
        if bot.username in update.message.new_chat_participant.username:
            message = "Salve" + (" a tutti" if update.message.chat.type == "group" else "") + "! Posso essere d'aiuto?"
            bot.send_message(update.message.chat_id, text=message)

    @staticmethod
    def sanitize_message(text, bot_username):
        return text.lower().replace(f'@{bot_username}', '').strip()
