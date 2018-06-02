import random
import re

from oracles.oracle import Oracle


class NumberOracle(Oracle):

    def handle(self):
        message = self.update.message.text
        message_wo_string_numbers = self.replace_text_numbers(message)
        numbers = self.extract_numbers_from_string(message_wo_string_numbers)
        len_number = len(numbers)

        if len_number == 1:
            self.show_numbers([random.randrange(numbers[0])])
        elif len_number == 2:
            self.show_numbers([random.randrange(min(numbers), max(numbers))])
        elif len_number > 2:
            self.choose_range_numbers(numbers)
        else:
            self.show_numbers([random.randrange(101)])

    def replace_text_numbers(self, text):
        rep = self.text_numbers()

        # use these three lines to do the replacement
        rep = dict((re.escape(k), str(v)) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
        return text

    @staticmethod
    def extract_numbers_from_string(text):
        return [int(s) for s in text.split() if s.isdigit()]

    def show_numbers(self, numbers):
        response = "Ecco qui: " + ", ".join(map(str, numbers))
        self.reply(response)

    def choose_range_numbers(self, numbers):
        message = self.update.message.text
        number_elems, *range_number = numbers

        if any(x in message for x in [" senza ripet"]):
            chosen_numbers = random.sample(range(min(range_number), max(range_number) + 1), number_elems)
        else:
            chosen_numbers = [random.randrange(min(range_number), max(range_number) + 1) for p in range(number_elems)]

        self.show_numbers(chosen_numbers)

    @staticmethod
    def text_numbers():
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
