import logging
from telegram.ext import Updater
from handlers import handlers
from bot import bot
from transactionschecker import TransactionsChecker

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    updater = Updater(bot=bot)

    dp = updater.dispatcher

    # Register handlers
    for handler in handlers:
        dp.add_handler(handler)

    # Tasks checker
    checker = TransactionsChecker()
    checker.daemon = True
    checker.start()
    # Start bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    checker.join()


if __name__ == '__main__':
    main()
