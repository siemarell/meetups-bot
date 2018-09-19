from sqlalchemy import Column, Integer, ForeignKey
import requests
from config import CHAIN, NODES
from .base_task import Task
from bot.messages import *


class SendWavesTask(Task):
    __tablename__ = 'task_send_waves'

    id = Column(Integer, ForeignKey('task.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

    reward = 1

    @staticmethod
    def name() -> str:
        return SEND_WAVES_NAME

    @property
    def result(self) -> str:
        return 'background'

    @property
    def description(self) -> str:
        return SEND_WAVES_DESCRIPTION

    @property
    def on_complete_msg(self) -> str:
        return SEND_WAVES_ON_COMPLETE_MSG

    def _verify(self) -> bool:
        # Todo: verify amount
        node_url = NODES.get(CHAIN)
        try:
            last_500_tx = requests.get(f'{node_url}/transactions/address/{self.user.address}/limit/500').json()[0]
            txs_to_app = [tx for tx in last_500_tx if
                          tx['type'] == 4 and
                          tx['recipient'] == APP_WAVES_ADDRESS and
                          tx['timestamp'] / 1000 > self.created.timestamp()]
            if txs_to_app:
                return True
        except Exception as e:
            pass
        return False

