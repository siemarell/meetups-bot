from threading import Thread
from time import sleep
from models import Task, TaskStatus, DexExchangeTask, SendWavesTask, User
from db import Session


class TransactionsChecker(Thread):
    def run(self) -> None:
        while True:
            session = Session()
            users_to_check = [user for user in session.query(User)
                              if user.active_task and user.active_task.result == 'background']

            for user in users_to_check:
                {
                    'SendWavesTask': self.check_send_waves_task,
                    'DexExchangeTask': self.check_dex_task
                }[type(user.active_task).__name__](user)

            session.close()
            sleep(5)

    def check_dex_task(self, user):
        pass

    def check_send_waves_task(self, user):
        pass
