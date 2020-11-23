import re
import os
import sys
import logging
import threading
import random
import time
from datetime import datetime, timedelta

import requests
import telegram
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters

from handlers import *
from handlers.values import *

BOT_TOKEN = os.environ.get('BOT_TOKEN')


logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('bot')


def run():
    updater = Updater(BOT_TOKEN)
    db = updater.dispatcher

    for handler in BaseHandler.__subclasses__():
        handler.build().assign(db)

    updater.start_polling()
    logger.info('Bot started')


if __name__ == '__main__':
    run()
