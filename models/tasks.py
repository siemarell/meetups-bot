from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Enum as AEnum
from enum import Enum, auto
from abc import abstractmethod
from config import CHAIN
from .base import Base
import pywaves as pw

pw.setChain(CHAIN)


class TaskStatus(Enum):
    CREATED = auto()
    ADDED = auto()
    SENT = auto()
    COMPLETED = auto()
    REWARDED = auto()


class Task(Base):  # , metaclass=ABCMeta):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(AEnum(TaskStatus))
    type = Column(String(20))
    user_id = Column(String, ForeignKey('user.chat_id'))

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': type
    }

    """Reward for task completion in WAVES"""
    reward = 0

    def __init__(self):
        self.status = TaskStatus.CREATED

    def verify(self, *args) -> bool:
        condition = self._verify(*args)
        if condition:
            self.status = TaskStatus.COMPLETED
        return condition

    @staticmethod
    @abstractmethod
    def name():
        return 'Basic task'

    @property
    @abstractmethod
    def result(self) -> str:
        """What should be an answer: message, image, background"""

    @property
    @abstractmethod
    def description(self) -> str:
        """Should contain task description"""

    @property
    @abstractmethod
    def on_complete_msg(self) -> str:
        """Should contain message, witch we send to user after he completes the task"""

    @abstractmethod
    def _verify(self, *args) -> bool:
        """Should verify the data and mark task completed if it passes"""


class GetUserAddressTask(Task):
    __tablename__ = 'task_get_address'

    id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    address = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'task_get_address',
    }

    @staticmethod
    def name():
        return 'Give address'

    @property
    def result(self):
        return 'message'

    @property
    def description(self):
        return f'Download Waves app and tell me your address'

    @property
    def on_complete_msg(self):
        return 'Congratulations! Now I have your address and you can choose next task'

    def _verify(self, address):
        validated = False
        try:
            validated = pw.validateAddress(address)
        except:
            pass
        if validated:
            self.address = address
        return validated


class DexExchangeTask(Task):
    __tablename__ = 'task_dex_exchange'

    id = Column(Integer, ForeignKey('task.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

    reward = 0.01

    @staticmethod
    def name():
        return 'Make DEX transaction'

    @property
    def result(self):
        return 'background'

    @property
    def description(self):
        return "Exchange WAVES to BTC using DEX"

    @property
    def on_complete_msg(self):
        return 'Congratulations! DEX task completed'

    def _verify(self) -> bool:
        return False


class SendWavesTask(Task):
    __tablename__ = 'task_send_waves'

    id = Column(Integer, ForeignKey('task.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

    reward = 0.01

    @staticmethod
    def name():
        return 'Make WAVES transaction'

    @property
    def result(self):
        return 'background'

    @property
    def description(self):
        return "Send x waves to y address!"

    @property
    def on_complete_msg(self):
        return "Completed send task"

    def _verify(self) -> bool:
        return False


TASK_TYPES = [GetUserAddressTask, DexExchangeTask, SendWavesTask]
