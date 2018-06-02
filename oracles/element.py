import random
import re

from oracles.oracle import Oracle


class ElementOracle(Oracle):

    def handle(self):
        message = self.update.message.text

        if "@" + self.bot.username in message:
            string = message.split("@" + self.bot.username, 1)[1].split(" ", 1)[1]
        else:
            string = message

        items = re.split(", | o | oppure ", string)
        if len(items) > 0:
            items[0] = items[0].split(" ")[-1]
        item_chosen = random.choice(items)
        response = random.choice(
            ["La scelta migliore è ", "Io vi consiglio ", "Sicuramente ", "Non ho dubbi: "]) + item_chosen.strip(" ")
        self.reply(response)
