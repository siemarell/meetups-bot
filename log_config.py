import logging
from logging.handlers import RotatingFileHandler

# # create file handler which logs even debug messages
fh = RotatingFileHandler('logs/log.log', maxBytes=1000000, backupCount=10)
# fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG, handlers=[ch, fh])

