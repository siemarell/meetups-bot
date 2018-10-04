import logging
from logging.handlers import RotatingFileHandler
from config import LOG_LEVEL, LOG_PATH

# # create file handler which logs even debug messages
fh = RotatingFileHandler(f'{LOG_PATH}/log.log', maxBytes=1000000, backupCount=10)
# fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=LOG_LEVEL, handlers=[ch, fh])

