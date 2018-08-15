from .base_task import Task, TaskStatus
from .get_user_address import GetUserAddressTask
from .send_waves import SendWavesTask
from .dex_exchange import DexExchangeTask
from .send_selfie import SendSelfieTask
from .find_user import FindUserTask

TASK_TYPES = [GetUserAddressTask, DexExchangeTask, SendWavesTask, SendSelfieTask, FindUserTask]
