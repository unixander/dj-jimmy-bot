import random
import logging
import time
import re
import os
from functools import partial

import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from .base import BaseHandler
from .values import (
    HELLO_WORDS,
    COMMANDS,
    HELLO_WORDS_INIT,
    HELLO_PICS_RESPONSE,
    WORDS_ANSWERS,
)
from apis import OpenWeatherMapApi

from datetime import datetime
random.seed(datetime.now())


class AnswerMessageHandler(BaseHandler):

    weather_api = OpenWeatherMapApi()
    telegram_handler = partial(MessageHandler, Filters.text)

    def __call__(self, bot, update, *args, **kwargs):
        text = re.sub(r'[.!?,()]', '', update.message.text.lower())
        self.single_words_answers(text, bot, update)\
            .weather(text, bot, update)\
            .hello_words(text, bot, update)

    def _check_hello_word(self, word, text):
        for text_word in text.split():
            if word.lower() == text_word.lower():
                return True
            if abs(len(word) - len(text_word)) < 3 and word in text_word:
                return True
        return False

    def hello_words(self, text, bot, update):
        if update.message.text and any(self._check_hello_word(w, text) for w in HELLO_WORDS_INIT):
            self.send_typing(bot, update)
            send_picture = random.choice([True, False])
            if send_picture:
                update.message.reply_photo(random.choice(HELLO_PICS_RESPONSE))
            else:
                update.message.reply_text(random.choice(HELLO_WORDS))
        return self

    def single_words_answers(self, text, bot, update):
        if text in WORDS_ANSWERS:
            self.send_typing(bot, update)
            update.message.reply_text(WORDS_ANSWERS[text])
        return self

    def weather(self, text, bot, update):
        if all(w in text for w in ('what', 'weather')):
            self.send_typing(bot, update)
            text = self.weather_api.get_default_cities()
            if text:
                update.message.reply_text(
                    text, parse_mode=telegram.ParseMode.MARKDOWN)
        return self
