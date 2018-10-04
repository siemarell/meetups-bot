from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import logging
from .base_task import Task
from bot.messages import *
from config import REWARD_VALUE, NODES, CHAIN
import requests

logger = logging.getLogger(__name__)


class FindUserTask(Task):
    __tablename__ = 'task_find_user'

    id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    user_to_find_id = Column(String, ForeignKey('user.chat_id'))

    user_to_find = relationship("User")

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

    reward = REWARD_VALUE

    def send_description(self, bot):
        super().send_description(bot)
        bot.send_photo(self.user.chat_id, self.user_to_find.image)

    @staticmethod
    def name() -> str:
        return FIND_USER_NAME

    @property
    def result(self) -> str:
        return 'background'

    @property
    def description(self) -> str:
        return FIND_USER_DESCRIPTION

    @property
    def on_complete_msg(self) -> str:
        return FIND_USER_ON_COMPLETE_MSG

    def _verify(self) -> bool:
        # Todo: verify amount
        node_url = NODES.get(CHAIN)
        try:
            last_500_tx = requests.get(f'{node_url}/transactions/address/{self.user.address}/limit/500').json()[0]
            txs_to_app = [tx for tx in last_500_tx if
                          tx['type'] == 4 and
                          tx['recipient'] == self.user_to_find.address and
                          tx['timestamp'] / 1000 > self.created.timestamp()]
            if txs_to_app:
                return True
        except Exception as e:
            logging.error(e)
        return False

