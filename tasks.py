from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum as AEnum
from enum import Enum, auto
from abc import abstractmethod, ABCMeta
import pywaves as pw

Base = declarative_base()


pw.setChain('testnet')


class TaskStatus(Enum):
    ADDED = auto()
    SENT = auto(),
    COMPLETED = auto()
    REWARDED = auto()


class Task(Base, metaclass=ABCMeta):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    status = Column(AEnum(TaskStatus))

    # def __init__(self, owner):
    #     self.owner = owner
    #     self.status = TaskStatus.ADDED

    @abstractmethod
    def verify(self, data)-> bool:
        """Should verify the data and mark task completed if it passes"""


class GetUserAddress(Task):
    def __init__(self):
        super().__init__()
        self.address = None

    def verify(self, address):
        if pw.validateAddress(address):
            self.address = address
            self.status = TaskStatus.DONE
            return True
        else:
            return False

