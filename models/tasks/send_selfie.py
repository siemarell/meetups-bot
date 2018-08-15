import face_recognition
import io
from sqlalchemy import Column, Integer, String, ForeignKey
from .base_task import Task
from messages import *


def face_locations(image):
    processed_image = face_recognition.load_image_file(io.BytesIO(image))
    return face_recognition.face_locations(processed_image)


class SendSelfieTask(Task):
    __tablename__ = 'task_send_selfie'

    id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    image_path = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

    reward = 1

    @staticmethod
    def name() -> str:
        return 'Send selfie'

    @property
    def result(self) -> str:
        return 'image'

    @property
    def description(self) -> str:
        return SEND_SELFIE_DESCRIPTION

    @property
    def on_complete_msg(self) -> str:
        return SEND_SELFIE_ON_COMPLETE_MSG

    def _verify(self, full_image) -> bool:
        # ToDo: Send message on false condition. User should know why image is bad
        image_file = full_image.get_file()
        image_bytes = image_file.download_as_bytearray()
        condition = len(face_locations(image_bytes)) == 1
        if condition:
            self.image_path = image_file.file_path
        return condition
