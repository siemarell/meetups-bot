import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import GetUserAddressTask, Task, TaskStatus, Base

MEMORY = 'sqlite:///:memory:'
DISK = 'sqlite:///storage.db'


class TestTasks(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine(MEMORY)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def test_create_get_address_task(self):
        task = GetUserAddressTask()
        task2 = GetUserAddressTask()
        self.session.add(task)
        self.session.add(task2)
        self.session.commit()
        tasks = [task for task in self.session.query(Task)]
        self.assertEqual(len(tasks), 2)

    def test_verify_address(self):
        task = GetUserAddressTask()
        self.assertTrue(task.verify('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1'))
        self.assertFalse(task.verify('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y'))

    def test_recover_from_db(self):
        task = GetUserAddressTask()
        task.verify('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1')
        self.session.add(task)
        self.session.commit()
        recovered = [task for task in self.session.query(Task)][-1]
        self.assertEqual(recovered.address, '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1')
        self.assertEqual(recovered.status, TaskStatus.COMPLETED)


if __name__ == '__main__':
    unittest.main()