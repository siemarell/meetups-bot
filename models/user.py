from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .sqla_base import Base
from .tasks import Task, GetUserAddressTask, SendSelfieTask, SendWavesTask, FindUserTask, TASK_TYPES, TaskStatus


class User(Base):
    __tablename__ = 'user'

    chat_id = Column(String, primary_key=True)
    tasks = relationship("Task", back_populates='user')

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def add_task(self, task: Task):
        task.status = TaskStatus.ADDED
        self.tasks.append(task)

    @property
    def active_task(self) -> Task:
        return next(filter(lambda task: task.status == TaskStatus.ADDED, self.tasks), None)

    @property
    def completed_tasks(self) -> [Task]:
        return list(filter(lambda task: task.status in [TaskStatus.COMPLETED, TaskStatus.REWARDED], self.tasks))

    @property
    def address(self) -> str:
        address_task: GetUserAddressTask = next(filter(lambda task: type(task) == GetUserAddressTask,
                                                       self.completed_tasks), None)
        if address_task:
            return address_task.address

    @property
    def image(self):
        selfie_task: SendSelfieTask = next(filter(lambda task: type(task) == SendSelfieTask,
                                                  self.completed_tasks), None)
        if selfie_task:
            return selfie_task.image_path

    @property
    def available_tasks(self) -> [str]:
        if not self.address:
            return [GetUserAddressTask]

        completed_types = [type(task) for task in self.completed_tasks]

        available = [TaskType.name() for TaskType in TASK_TYPES if TaskType not in completed_types]
        # Make find user task available only if user has completed send selfie task and there is another user
        # that has completed it
        return available
