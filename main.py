import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import startHandler, helpHandler, menuHandler, menuCallbackHandler, unknownCommandHandler, messageHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    updater = Updater('558192444:AAHXehbN2ItrZahpH_mDqig76cvcLspFtVg')

    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(startHandler)
    dp.add_handler(helpHandler)
    dp.add_handler(menuHandler)
    dp.add_handler(menuCallbackHandler)
    dp.add_handler(unknownCommandHandler)
    dp.add_handler(messageHandler)

    # Start bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
