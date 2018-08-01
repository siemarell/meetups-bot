import logging
from telegram.ext import Updater
from handlers import handlers
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    updater = Updater('558192444:AAHXehbN2ItrZahpH_mDqig76cvcLspFtVg')

    dp = updater.dispatcher

    # Register handlers
    for handler in handlers:
        dp.add_handler(handler)

    # Start bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
