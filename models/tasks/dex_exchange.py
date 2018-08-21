from sqlalchemy import Column, Integer, ForeignKey
import requests
from config import CHAIN, NODES
from .base_task import Task
from bot.messages import *


class DexExchangeTask(Task):
    __tablename__ = 'task_dex_exchange'

    id = Column(Integer, ForeignKey('task.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

    reward = 1

    @staticmethod
    def name() -> str:
        return 'Make DEX transaction'

    @property
    def result(self) -> str:
        return 'background'

    @property
    def description(self) -> str:
        return DEX_EXCHANGE_DESCRIPTION

    @property
    def on_complete_msg(self) -> str:
        return DEX_EXCHANGE_ON_COMPLETE_MSG

    def _verify(self) -> bool:
        # Todo: verify amount
        node_url = NODES.get(CHAIN)
        try:
            last_500_tx = requests.get(f'{node_url}/transactions/address/{self.user.address}/limit/500').json()[0]
            exchange = [tx for tx in last_500_tx if
                        tx['type'] == 7
                        and
                        (tx['order1']['assetPair'] == {'amountAsset': None,
                                                       'priceAsset': '8LQW8f7P5d5PZM7GtZEBgaqRPGSzS3DfPuiXrURJ4AJS'} or
                         tx['order2']['assetPair'] == {'amountAsset': None,
                                                       'priceAsset': '8LQW8f7P5d5PZM7GtZEBgaqRPGSzS3DfPuiXrURJ4AJS'})
                        and
                        tx['timestamp'] / 1000 > self.created.timestamp()]
            if len(exchange) > 0:
                return True
        except:
            pass
        return False
