from sqlalchemy import Column, Integer, String, ForeignKey
from config import CHAIN
from messages import *
from .base_task import Task
import pywaves as pw

pw.setChain(CHAIN)


class GetUserAddressTask(Task):
    __tablename__ = 'task_get_address'

    id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    address = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'task_get_address',
    }

    @staticmethod
    def name() -> str:
        return 'Give address'

    @property
    def result(self) -> str:
        return 'message'

    @property
    def description(self) -> str:
        return GET_USER_ADDRESS_DESCRIPTION

    @property
    def on_complete_msg(self) -> str:
        return GET_USER_ADDRESS_ON_COMPLETE_MSG

    def _verify(self, address):
        validated = False
        try:
            validated = pw.validateAddress(address)
        except:
            pass
        if validated:
            self.address = address
        return validated

