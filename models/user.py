from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base, Task, GetUserAddressTask, DexExchangeTask, SendWavesTask, TaskStatus


class User(Base):
    __tablename__ = 'user'

    chat_id = Column(String, primary_key=True)
    tasks = relationship("Task", backref='user', remote_side=[chat_id])

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def add_task(self, task: Task):
        task.status = TaskStatus.ADDED
        self.tasks.append(task)

    @property
    def active_task(self) -> Task:
        return next(filter(lambda task: task.status == TaskStatus.ADDED, self.tasks), None)

    @property
    def completed_tasks(self):
        return list(filter(lambda task: task.status == TaskStatus.COMPLETED, self.tasks))

    @property
    def address(self):
        address_task: GetUserAddressTask = next(filter(lambda task: type(task) == GetUserAddressTask,
                                                       self.completed_tasks), None)
        if address_task:
            return address_task.address

    @property
    def available_tasks(self):
        if not self.address:
            return [GetUserAddressTask]

        completed_types = [type(task) for task in self.completed_tasks]
        return [str(TaskType) for TaskType in [GetUserAddressTask, DexExchangeTask, SendWavesTask]
                if TaskType not in completed_types]
