from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as AEnum
import datetime
from enum import Enum, auto
from abc import abstractmethod
from ..sqla_base import Base
from rewarder import rewarder


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
    created = Column(TIMESTAMP)
    type = Column(String(20))
    user_id = Column(String, ForeignKey('user.chat_id'))

    user = relationship("User", back_populates='tasks')

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': type
    }

    """Reward for task completion in WAVES"""
    reward = 0

    def __init__(self):
        self.status = TaskStatus.CREATED
        self.created = datetime.datetime.now()

    def verify(self, *args) -> bool:
        condition = self._verify(*args)
        if condition:
            self.status = TaskStatus.COMPLETED
            if self.reward > 0:
                try:
                    rewarder.send_reward(self.user.address, self.reward)
                    self.status = TaskStatus.REWARDED
                except Exception as e:
                    print(e)
        return condition

    @staticmethod
    @abstractmethod
    def name() -> str:
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
