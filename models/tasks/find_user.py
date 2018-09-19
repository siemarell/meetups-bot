from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base_task import Task
from bot.messages import *


class FindUserTask(Task):
    __tablename__ = 'task_find_user'

    id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    user_to_find_id = Column(String, ForeignKey('user.chat_id'))

    user_to_find = relationship("User")

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

    reward = 1

    def send_description(self, bot):
        super().send_description(bot)
        bot.send_photo(self.user.chat_id, self.user_to_find.image)

    @staticmethod
    def name() -> str:
        return FIND_USER_NAME

    @property
    def result(self) -> str:
        return 'message'

    @property
    def description(self) -> str:
        return FIND_USER_DESCRIPTION

    @property
    def on_complete_msg(self) -> str:
        return FIND_USER_ON_COMPLETE_MSG

    def _verify(self, address) -> bool:
        return address == self.user_to_find.address

