import telegram
import logging
from threading import Thread
from time import sleep
from models import User
from db import Session
from config import CHECK_INTERVAL

logger = logging.getLogger(__name__)


class Checker(Thread):
    def __init__(self, bot: telegram.Bot):
        super().__init__()
        self.bot = bot

    def run(self) -> None:
        while True:
            try:
                session = Session()
                users_to_check: [User] = [user for user in session.query(User)
                                          if user.active_task and user.active_task.result == 'background']
                logger.info(f'{len(users_to_check)} active background tasks')
                for user in users_to_check:
                    task = user.active_task
                    if task.verify():
                        self.bot.send_message(user.chat_id, task.on_complete_msg)
                        session.commit()
                session.close()
                sleep(CHECK_INTERVAL)
            except Exception as e:
                logger.error(e)
