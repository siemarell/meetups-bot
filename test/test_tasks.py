import unittest
import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tasks import Base, GetUserAddressTask, Task


class TestTasks(unittest.TestCase):
    # engine = create_engine('sqlite:///:memory:')
    # Session = sessionmaker(bind=engine)

    def setUp(self):
        self.engine = create_engine('sqlite:///storage.db')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def test_create_get_address_task(self):
        task = GetUserAddressTask()
        self.session.add(task)
        self.session.commit()
        tasks = [task for task in self.session.query(Task)]
        pass

        #self.assertEqual(db.get_last_update_index(), 0)
    #
    # def test_update(self):
    #     db.update_last_update_index(10)
    #     self.assertEqual(db.get_last_update_index(), 10)
    #
    # @classmethod
    # def tearDownClass(cls):
    #     db.update_last_update_index(0)

if __name__ == '__main__':
    unittest.main()