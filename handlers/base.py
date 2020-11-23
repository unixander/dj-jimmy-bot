import time
import telegram
import logging


class BaseHandler(object):

    telegram_handler = None
    typing_time = 5

    @classmethod
    def build(cls):
        return cls()

    def __call__(self, bot, update, *args, **kwargs):
        self.send_typing(bot, update)

    def send_typing(self, bot, update):
        passed_time = 0
        while passed_time < self.typing_time:
            bot.send_chat_action(
                chat_id=update.message.chat_id,
                action=telegram.ChatAction.TYPING
            )
            time_to_sleep = min([self.typing_time, 6])
            time.sleep(time_to_sleep)
            passed_time += time_to_sleep

    def assign(self, dispatcher):
        logging.getLogger(__name__).info('Handler %s was registered', self.__class__.__name__)
        dispatcher.add_handler(self.telegram_handler(self))
