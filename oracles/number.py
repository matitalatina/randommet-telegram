import random
import re


class NumberOracle(object):
    @classmethod
    def reply(cls, bot, update):
        message = update.message.text
        message_wo_string_numbers = cls.replace_text_numbers(message)
        numbers = cls.extract_numbers_from_string(message_wo_string_numbers)
        len_number = len(numbers)

        if len_number == 1:
            cls.show_numbers(bot, update, [random.randrange(numbers[0])])
        elif len_number == 2:
            cls.show_numbers(bot, update, [random.randrange(min(numbers), max(numbers))])
        elif len_number > 2:
            cls.choose_range_numbers(bot, update, numbers)
        else:
            cls.show_numbers(bot, update, [random.randrange(101)])

    @classmethod
    def replace_text_numbers(cls, text):
        rep = cls.text_numbers()

        # use these three lines to do the replacement
        rep = dict((re.escape(k), str(v)) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
        return text

    @classmethod
    def extract_numbers_from_string(cls, text):
        return [int(s) for s in text.split() if s.isdigit()]

    @classmethod
    def show_numbers(cls, bot, update, numbers):
        response = "Ecco qui: " + ", ".join(map(str, numbers))
        bot.send_message(update.message.chat_id, text=response)

    @classmethod
    def choose_range_numbers(cls, bot, update, numbers):
        message = update.message.text
        number_elems, *range_number = numbers

        if any(x in message for x in [" senza ripet"]):
            chosen_numbers = random.sample(range(min(range_number), max(range_number) + 1), number_elems)
        else:
            chosen_numbers = [random.randrange(min(range_number), max(range_number) + 1) for p in range(number_elems)]

        cls.show_numbers(bot, update, chosen_numbers)

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
