from db import Session
from models import User, GetUserAddressTask
import logging
from functools import wraps

logger = logging.getLogger(__name__)


def with_user(func):
    @wraps(func)
    def inner(bot, update):
        chat_id = update.effective_user.id
        session = Session()
        user: User = session.query(User).filter(User.chat_id == chat_id).one_or_none()
        if not user:
            logger.info(f'New user {chat_id}')
            # Initialize user and add first task
            user = User(chat_id)
            first_task = GetUserAddressTask()
            user.add_task(first_task)
            session.add(user)

        result = None
        try:
            result = func(bot, update, user)
            session.commit()
        except Exception as e:
            logger.error(e)
        finally:
            session.close()
            return result
    return inner

