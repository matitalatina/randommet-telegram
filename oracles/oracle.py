from abc import abstractmethod


class Oracle(object):
    def __init__(self, bot, update):
        self.bot = bot
        self.update = update

    @abstractmethod
    def handle(self):
        raise NotImplementedError()

    def reply(self, response):
        self.bot.send_message(self.update.message.chat_id, text=response)
