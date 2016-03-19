# Randommet - Telegram Bot
This is the heart of my Telegram Bot Randommet.

## Features
This is the translation of the help message

- Oracle: end the phrase with "?".  
  Example: _Should I Study today?_
- List: write some choices divided by comma ",". It will choose the best choice.  
  Example: _cinema, bowling, pub_
- Numbers: "_Choose a number between 0 and 25_", "_Choose 6 numbers without repetitions between 1 and 90_", "_Choose twelve numbers_", "_Choose a number until 10_".
- Colors: "_Choose a color_"


Remember to call Randommet if you want to use it in a group. You can do that writing `@[bot.username]` at the beginning of the message. Change `bot.username` with the name of your modded bot.

## Requirements

- Python 3
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

## Getting started

Install dependencies

```$ pip install python-telegram-bot```

Add your token bot in the line

```updater = Updater("***YOUR_TOKEN_HERE***")```

Start it

```$ python3 randommet.py```

In production mode use it instead (no log, you can close your terminal):

```nohup python3 randommet.py  </dev/null >/dev/null 2>&1```

Enjoy!

## FAQ

- _Why the bot replies in Italian?!_ Because all my friends and I are Italians! But I wrote the code in English, so feel free to change the reply messages with your language! ;) 