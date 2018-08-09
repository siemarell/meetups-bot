from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import ENV

MEMORY = 'sqlite:///:memory:'
DISK = 'sqlite:///storage.db'

engine = create_engine(DISK)

if ENV == 'DEV':
    Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(engine)
