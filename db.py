from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MEMORY = 'sqlite:///:memory:'
DISK = 'sqlite:///storage.db'

# Todo: use process.env == dev instead
STORAGE = DISK

engine = create_engine(STORAGE)
if STORAGE == DISK:
    from models import Base
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
Session = sessionmaker(engine)
