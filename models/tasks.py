from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Enum as AEnum
from enum import Enum, auto
from abc import abstractmethod, ABCMeta
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
        'polymorphic_identity': 'task',
        'polymorphic_on': type
    }

    def __init__(self):
        self.status = TaskStatus.CREATED

    @abstractmethod
    def verify(self, data) -> bool:
        """Should verify the data and mark task completed if it passes"""


class GetUserAddressTask(Task):
    __tablename__ = 'task_get_address'

    id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    address = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'task_get_user_address',
    }

    def verify(self, address):
        if pw.validateAddress(address):
            self.address = address
            self.status = TaskStatus.COMPLETED
            return True
        else:
            return False