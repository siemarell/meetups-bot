from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Enum as AEnum
from enum import Enum, auto
from abc import abstractmethod
import pywaves as pw
from .base import Base


pw.setChain('testnet')


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

    def __init__(self):
        self.status = TaskStatus.CREATED

    @staticmethod
    @abstractmethod
    def name():
        return 'Basic task'

    @property
    @abstractmethod
    def result(self):
        """What should be an answer: message, image, background"""

    @property
    @abstractmethod
    def description(self):
        """Should contain task description"""

    @property
    @abstractmethod
    def on_complete_msg(self):
        """Should contain message, witch we send to user after he completes the task"""

    @abstractmethod
    def verify(self, data) -> bool:
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

    def verify(self, address):
        validated = False
        try:
            validated = pw.validateAddress(address)
        except:
            pass
        if validated:
            self.address = address
            self.status = TaskStatus.COMPLETED
        return validated


class DexExchangeTask(Task):
    __tablename__ = 'task_dex_exchange'

    id = Column(Integer, ForeignKey('task.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

    @staticmethod
    def name():
        return 'Make DEX transaction'

    @property
    def result(self):
        return 'message'

    @property
    def description(self):
        return "Exchange WAVES to BTC using DEX"

    @property
    def on_complete_msg(self):
        return 'Congratulations! DEX task completed'

    def verify(self, data) -> bool:
        return data == 'Hello!'


class SendWavesTask(Task):
    __tablename__ = 'task_send_waves'

    id = Column(Integer, ForeignKey('task.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

    @staticmethod
    def name():
        return 'Make WAVES transaction'

    @property
    def result(self):
        return 'message'

    @property
    def description(self):
        return "Send x waves to y address!"

    @property
    def on_complete_msg(self):
        return "Completed send task"

    def verify(self, data) -> bool:
        return data == 'Bye!'


TASK_TYPES = [GetUserAddressTask, DexExchangeTask, SendWavesTask]
