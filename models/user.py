from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base, Task, TaskStatus


class User(Base):
    __tablename__ = 'user'

    chat_id = Column(String, primary_key=True)
    address = Column(String)
    tasks = relationship("Task", backref='user', remote_side=[chat_id])

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def add_task(self, task: Task):
        task.status = TaskStatus.ADDED
        self.tasks.append(task)

    @property
    def active_task(self):
        return next(filter(lambda task: task.status == TaskStatus.SENT, self.tasks), None)
