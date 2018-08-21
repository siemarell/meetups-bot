import log_config
import logging
from telegram.ext import Updater
from handlers import handlers
from bot import bot
from checker import Checker

logger = logging.getLogger(__name__)


def main():
    updater = Updater(bot=bot)

    dp = updater.dispatcher

    # Register handlers
    for handler in handlers:
        dp.add_handler(handler)
    logger.info('Handlers registered')

    # Tasks checker
    checker = Checker(bot)
    checker.daemon = True
    checker.start()
    logger.info('Checker started')

    # Start bot
    updater.start_polling()
    logger.info('Bot started')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
