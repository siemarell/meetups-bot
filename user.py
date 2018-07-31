from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    chat_id = Column(String, primary_key=True)
    address = Column(String)
    tasks = Column()

    # def __init__(self, chat_id):
    #     self.chat_id = chat_id
    #     self.address = None
    #     self.tasks = []

