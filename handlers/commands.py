import random
import logging
import time
import re
from functools import partial

import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from .base import BaseHandler
from .values import HELLO_WORDS, COMMANDS, HELLO_WORDS_INIT, HELLO_PICS_RESPONSE, WORDS_ANSWERS
from apis import OpenWeatherMapApi, ExchangeRatesApi, VatApi


class StartHandler(BaseHandler):

    telegram_handler = partial(CommandHandler, 'start')

    def __call__(self, bot, update, *args, **kwargs):
        super().__call__(bot, update, *args, **kwargs)
        update.message.reply_text('DJ Jimmy in da house!')


class HelloHandler(BaseHandler):

    telegram_handler = partial(CommandHandler, 'hello')

    def __call__(self, bot, update, *args, **kwargs):
        super().__call__(bot, update, *args, **kwargs)
        update.message.reply_text(random.choice(HELLO_WORDS))


class ErrorHandler(BaseHandler):

    logger = logging.getLogger('bot')

    def __call__(self, bot, update, error, *args, **kwargs):
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def assign(self, dispatcher):
        dispatcher.add_error_handler(self)


class WeatherHandler(BaseHandler):

    api = OpenWeatherMapApi()
    telegram_handler = partial(CommandHandler, 'weather')

    def __call__(self, bot, update, *args, **kwargs):
        super().__call__(bot, update, *args, **kwargs)
        text = ' '.join(update.message.text.strip().split()[1:])
        if not text:
            text = self.api.get_default_cities()
            if text:
                update.message.reply_text(
                    text, parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                update.message.reply_text('Укажи город')
        else:
            text = self.api.get_city_message(text)
            if text:
                update.message.reply_text(
                    text, parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                update.message.reply_text(
                    'Извини, братюнь, попробуй уточнить запрос.')


class MappedCommandsHandler(BaseHandler):

    telegram_handler = CommandHandler
    commands_mapping = COMMANDS

    def build_handler(self, text):
        def inner(bot, update):
            if isinstance(text, list):
                update.message.reply_text(random.choice(text))
            else:
                update.message.reply_text(text)
        return inner

    def assign(self, dispatcher):
        for command, value in self.commands_mapping.items():
            dispatcher.add_handler(
                self.telegram_handler(command, self.build_handler(value)))


# class CurrencyHandler(BaseHandler):

#     api = ExchangeRatesApi()
#     telegram_handler = partial(CommandHandler, 'currency')

#     def __call__(self, bot, update, *args, **kwargs):
#         super().__call__(bot, update, *args, **kwargs)
#         reply = self.api.get_currencies_message()
#         if reply:
#             update.message.reply_text(reply)


class VatHandler(BaseHandler):

    api = VatApi()
    telegram_handler = partial(CommandHandler, 'vat')

    def __call__(self, bot, update, *args, **kwargs):
        super().__call__(bot, update, *args, **kwargs)
        code = ' '.join(update.message.text.strip().split()[1:])
        response = self.api.get_vat_rate_by_code(code)
        update.message.reply_text(response, parse_mode=telegram.ParseMode.HTML)
