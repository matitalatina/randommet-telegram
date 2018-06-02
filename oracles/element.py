import random
import re


class ElementOracle(object):

    @classmethod
    def reply(cls, bot, update):
        message = update.message.text

        if "@" + bot.username in message:
            string = message.split("@" + bot.username, 1)[1].split(" ", 1)[1]
        else:
            string = message

        items = re.split(", | o | oppure ", string)
        if len(items) > 0:
            items[0] = items[0].split(" ")[-1]
        item_chosen = random.choice(items)
        response = random.choice(
            ["La scelta migliore è ", "Io vi consiglio ", "Sicuramente ", "Non ho dubbi: "]) + item_chosen.strip(" ")
        bot.send_message(update.message.chat_id, text=response)