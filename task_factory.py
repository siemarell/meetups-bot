import random
from models import TASK_TYPES, Task, FindUserTask, User, GetUserAddressTask
from bot.messages import ALREADY_COMPLETED_MSG, NOT_AVAILABLE_TASK_MSG
from db import Session


class TaskFactory:
    @staticmethod
    def create_task(task_name, user: User) -> Task:
        if task_name in (task.name() for task in user.completed_tasks):
            raise AlreadyCompletedTaskException(ALREADY_COMPLETED_MSG % task_name)

        available_tasks = TaskFactory.available_tasks(user)
        if task_name not in available_tasks:
            raise NotAvailableTaskException(NOT_AVAILABLE_TASK_MSG % task_name)

        # Find task class and create instance
        task = next(filter(lambda x: x.name() == task_name, TASK_TYPES))()

        # For find user task we need to find another random user with image
        if type(task) == FindUserTask:
            if not user.image:
                raise NotAvailableTaskException('Please complete send selfie task first')
            session = Session.object_session(user)
            # ToDo: we need to have another user with selfie
            # available_users = session.query(User).filter(User.chat_id != self.chat_id).all()
            chat_id = user.chat_id
            available_users = [user for user in session.query(User).all() if user.image and user.chat_id != chat_id]
            if len(available_users) == 0:
                raise NotEnoughUsersException(NOT_AVAILABLE_TASK_MSG % task_name)
            user_to_find = random.choice(available_users)
            task.user_to_find = user_to_find
        return task

    @staticmethod
    def available_tasks(user: User):
        if not user.address:
            return [GetUserAddressTask.name()]

        completed_types = [type(task) for task in user.completed_tasks]

        available = [TaskType.name() for TaskType in TASK_TYPES if TaskType not in completed_types]
        # Make find user task available only if user has completed send selfie task and there is another user
        # that has completed it
        return available


class TaskCreationException(Exception):
    pass


class NotEnoughUsersException(TaskCreationException):
    pass


class NotAvailableTaskException(TaskCreationException):
    pass


class AlreadyCompletedTaskException(TaskCreationException):
    pass
