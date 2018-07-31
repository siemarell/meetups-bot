import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Task

MEMORY = 'sqlite:///:memory:'
DISK = 'sqlite:///storage.db'


class TestUser(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine(DISK)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def test_create_user(self):
        user = User('abracadabra')
        user2 = User('abracadabra1')
        self.session.add(user)
        self.session.add(user2)
        self.session.commit()
        users = [user for user in self.session.query(User)]
        self.assertEqual(len(users), 2)

    def test_add_task(self):
        user = User('abracadabra')
        task = Task()
        user.tasks.append(task)
        self.assertEqual(len(user.tasks), 1)

    def test_recover(self):
        user = User('abracadabra')
        task = Task()
        user.tasks.append(task)
        self.session.add(user)
        self.session.commit()
        del user, task
        user = [user for user in self.session.query(User)][0]
        self.assertEqual(len(user.tasks), 1)


if __name__ == '__main__':
    unittest.main()