import telegram
from threading import Thread
from time import sleep
from models import Task, TaskStatus, DexExchangeTask, SendWavesTask, User
from db import Session
from config import CHAIN, CHECK_INTERVAL


class Checker(Thread):
    def __init__(self, bot: telegram.Bot):
        super().__init__()
        self.bot = bot

    def run(self) -> None:
        while True:
            session = Session()
            users_to_check: [User] = [user for user in session.query(User)
                                      if user.active_task and user.active_task.result == 'background']

            for user in users_to_check:
                task = user.active_task
                if task.verify():
                    self.bot.send_message(user.chat_id, task.on_complete_msg)
                    session.commit()
            session.close()
            sleep(CHECK_INTERVAL)
